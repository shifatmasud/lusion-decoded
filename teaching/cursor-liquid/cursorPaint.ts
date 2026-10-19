// Original teaching code (MIT). Not Lusion's code. See handbook chapter 14, section S.9.
import * as THREE from 'three';
import { FullScreenQuad } from 'three/examples/jsm/postprocessing/Pass.js';

const paintFrag = /* glsl */ `
uniform sampler2D uPrev; uniform vec2 uTexel, uA, uB, uVel;
uniform float uRadius, uAdvect; uniform vec3 uDecay;
varying vec2 vUv;
void main() {
  vec2 px = vUv / uTexel, ab = uB - uA;
  float t = clamp(dot(px - uA, ab) / max(dot(ab, ab), 1e-4), 0., 1.);
  float brush = uRadius > 0. ? 1. - smoothstep(0., uRadius, length(px - uA - ab * t)) : 0.;
  vec2 flow = texture2D(uPrev, vUv).xy;                 // signed, float target
  vec4 s = texture2D(uPrev, vUv - flow * uAdvect * uTexel); // carry paint along its motion
  s.xy *= uDecay.x; s.z *= uDecay.y; s.w *= uDecay.z;
  s.xy += uVel * brush;
  s.zw = min(s.zw + brush, 1.);
  gl_FragColor = s;
}`;

export const distortFrag = /* glsl */ `
uniform sampler2D tDiffuse, uPaint; uniform vec2 uTexel; uniform float uStrength;
varying vec2 vUv;
void main() {
  vec4 p = texture2D(uPaint, vUv);
  float w = 0.5 * (p.z + p.w);
  vec2 stepUv = -p.xy * w * uStrength * uTexel;
  vec3 c = vec3(0.); vec2 uv = vUv;
  for (int i = 0; i < 8; i++) { c += texture2D(tDiffuse, uv).rgb; uv += stepUv; }
  c /= 8.;
  float wake = (1. - smoothstep(0., .5, w)) * min(length(p.xy) * .05, 1.);
  c += wake * .15 * (.5 + .5 * cos(6.2831 * (dot(p.xy, vec2(.02)) + vec3(0., .33, .67))));
  gl_FragColor = vec4(c, 1.);
}`;

const vert = `varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0., 1.); }`;

export class CursorPaint {
  private a: THREE.WebGLRenderTarget; private b: THREE.WebGLRenderTarget;
  private quad: FullScreenQuad; private mat: THREE.ShaderMaterial;
  private last = new THREE.Vector2(-1, -1); private vel = new THREE.Vector2();
  texture!: THREE.Texture;

  constructor(private gl: THREE.WebGLRenderer, w: number, h: number, private scale = 0.25) {
    const opts = { type: THREE.HalfFloatType, depthBuffer: false };
    this.a = new THREE.WebGLRenderTarget(1, 1, opts);
    this.b = new THREE.WebGLRenderTarget(1, 1, opts);
    this.mat = new THREE.ShaderMaterial({
      vertexShader: vert, fragmentShader: paintFrag,
      uniforms: { uPrev: { value: null }, uTexel: { value: new THREE.Vector2() },
        uA: { value: new THREE.Vector2() }, uB: { value: new THREE.Vector2() },
        uVel: { value: new THREE.Vector2() }, uRadius: { value: 0 },
        uAdvect: { value: 0.6 }, uDecay: { value: new THREE.Vector3() } },
    });
    this.quad = new FullScreenQuad(this.mat);
    this.setSize(w, h);
  }

  setSize(w: number, h: number) {
    const pw = Math.max(1, Math.floor(w * this.scale)), ph = Math.max(1, Math.floor(h * this.scale));
    this.a.setSize(pw, ph); this.b.setSize(pw, ph);
    this.mat.uniforms.uTexel.value.set(1 / pw, 1 / ph);
  }

  /** pointer in 0..1 UV (y up), dt in seconds */
  update(pointer: THREE.Vector2, dt: number, maxRadiusPx = 18) {
    [this.a, this.b] = [this.b, this.a];                     // ping-pong
    const u = this.mat.uniforms, pw = this.a.width, ph = this.a.height;
    const to = new THREE.Vector2(pointer.x * pw, pointer.y * ph);
    if (this.last.x < 0) this.last.copy(to);
    const move = to.clone().sub(this.last);
    const f = dt * 60;
    this.vel.multiplyScalar(Math.pow(0.8, f)).add(move);      // smoothed brush velocity
    u.uA.value.copy(this.last); u.uB.value.copy(to);
    u.uRadius.value = THREE.MathUtils.clamp(move.length() / 10, 0, 1) * maxRadiusPx;
    u.uVel.value.copy(this.vel);
    u.uDecay.value.set(Math.pow(0.975, f), Math.pow(0.95, f), Math.pow(0.8, f));
    u.uPrev.value = this.b.texture;
    this.gl.setRenderTarget(this.a); this.quad.render(this.gl); this.gl.setRenderTarget(null);
    this.texture = this.a.texture;
    this.last.copy(to);
  }
}
