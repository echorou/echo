// ECHO addition: an online tabular Q-learning caretaker, not a language model.
export const actions=[{label:'Hold a steady environment',light:0.35,mut:0.002},{label:'Offer more light',light:0.65,mut:0.002},{label:'Try a quieter environment',light:0.18,mut:0.001},{label:'Explore a little variation',light:0.42,mut:0.008}];
export class Caretaker{
 constructor(saved={}){this.q=saved.q||{};this.updates=saved.updates||0;this.last=null;this.reward=0;this.action=0;}
 state(m){return `${m.ratio<0.65?0:m.ratio>1.2?2:1}:${m.energyPerMass<0.2?0:m.energyPerMass>0.55?2:1}`;}
 values(s){return this.q[s]||(this.q[s]=[0,0,0,0]);}
 observe(m,random=Math.random){const s=this.state(m),qs=this.values(s);if(this.last){this.reward=Math.max(-1,Math.min(1,(m.mass-this.last.mass)/Math.max(1,this.last.mass)*4+(m.mass>1?0.04:-0.4)));const prev=this.values(this.last.state);prev[this.last.action]+=0.22*(this.reward+0.85*Math.max(...qs)-prev[this.last.action]);this.updates++;}const epsilon=Math.max(0.12,0.5/Math.sqrt(1+this.updates/10));this.action=random()<epsilon?Math.floor(random()*4):qs.indexOf(Math.max(...qs));this.last={state:s,action:this.action,mass:m.mass};return actions[this.action];}
 serialize(){return {q:this.q,updates:this.updates};}
}
