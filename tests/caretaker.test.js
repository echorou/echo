import test from 'node:test';
import assert from 'node:assert/strict';
import {Caretaker} from '../dist/js/caretaker.js';
import {makeWorld} from '../dist/js/worlds.js';
test('positive survival outcome changes action values; a checkpoint retains learning',()=>{const c=new Caretaker();c.observe({mass:100,ratio:1,energyPerMass:.4},()=>.99);c.observe({mass:115,ratio:1.15,energyPerMass:.4},()=>.99);assert.equal(c.updates,1);assert.ok(c.q['1:1'][0]>0);const restored=new Caretaker(JSON.parse(JSON.stringify(c.serialize())));assert.deepEqual(restored.q,c.q);assert.equal(restored.updates,1);});
test('collapse receives negative reward; values stay finite over repeated losses',()=>{const c=new Caretaker();c.observe({mass:100,ratio:1,energyPerMass:.4},()=>.99);c.observe({mass:0,ratio:0,energyPerMass:0},()=>.99);assert.equal(c.reward,-1);for(let i=0;i<100;i++)c.observe({mass:0,ratio:0,energyPerMass:0},()=>.99);assert.ok(Object.values(c.q).flat().every(Number.isFinite));});
test('seed presets create finite state and repeat with the same seed',()=>{for(const name of ['glider','garden','collide','soup']){const a=makeWorld(name,128,128,{seed:260924});const b=makeWorld(name,128,128,{seed:260924});assert.deepEqual(a,b);assert.equal(a.s0.length,65536);assert.ok(a.s0.every(Number.isFinite));assert.ok(a.s0.some((v,i)=>i%4===0&&v>0));}});

test('saved Q tables are isolated and restored random decisions continue reproducibly',()=>{const c=new Caretaker();const m={mass:100,ratio:1,energyPerMass:.4};c.observe(m);const saved=c.serialize(),snapshot=JSON.stringify(saved);const clone=new Caretaker(saved);assert.deepEqual(c.observe({...m,mass:105}),clone.observe({...m,mass:105}));assert.deepEqual(c.serialize(),clone.serialize());assert.equal(JSON.stringify(saved),snapshot);});
