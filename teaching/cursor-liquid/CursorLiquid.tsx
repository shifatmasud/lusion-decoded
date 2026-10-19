// Original teaching code (MIT). Not Lusion's code. See handbook chapter 14, section S.9.
import { useFrame, useThree } from '@react-three/fiber';
import { EffectComposer, RenderPass, ShaderPass } from 'three-stdlib';
import { useEffect, useMemo } from 'react';
import * as THREE from 'three';
import { CursorPaint, distortFrag } from './cursorPaint';

export function CursorLiquid({ strength = 12 }) {
  const { gl, scene, camera, size, pointer } = useThree();
  const paint = useMemo(() => new CursorPaint(gl, size.width, size.height), [gl]);
  const [composer, pass] = useMemo(() => {
    const c = new EffectComposer(gl);
    c.addPass(new RenderPass(scene, camera));
    const p = new ShaderPass({
      uniforms: { tDiffuse: { value: null }, uPaint: { value: null },
        uTexel: { value: new THREE.Vector2() }, uStrength: { value: strength } },
      vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }`,
      fragmentShader: distortFrag,
    });
    c.addPass(p);
    return [c, p];
  }, [gl, scene, camera]);

  useEffect(() => {
    paint.setSize(size.width, size.height);
    composer.setSize(size.width, size.height);
    pass.uniforms.uTexel.value.set(4 / size.width, 4 / size.height); // paint texel at 1/4 res
  }, [size]);

  const uv = useMemo(() => new THREE.Vector2(), []);
  useFrame((_, dt) => {
    uv.set(pointer.x * 0.5 + 0.5, pointer.y * 0.5 + 0.5);
    paint.update(uv, Math.min(dt, 1 / 20));
    pass.uniforms.uPaint.value = paint.texture;
    composer.render(dt);
  }, 1); // priority 1: R3F stops its own render, we render through the composer
  return null;
}
