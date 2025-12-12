import{U as oe,V as f,W as C,X as k,Y as Qe,Z as Mt,$ as jt,a0 as Ut,d as ne,a1 as rt,a2 as Ue,a3 as Nt,r as D,a4 as dt,c as N,a5 as ut,a6 as ct,j as de,n as It,a7 as Xe,a8 as Pt,a9 as Ye,aa as $,ab as Et,ac as Ht,ad as At,ae as Lt,af as Ot,ag as ie,ah as Fe,ai as Be,z as Oe,aj as et,ak as tt,al as Kt,am as le,an as Ke,ao as J,ap as We,aq as se,ar as Wt,as as Xt,o as y,b as z,e as w,w as T,v as g,a as m,L as qe,g as i,F as pe,m as P,at as Yt,E as vt,l as qt,h as A,au as Zt,av as at,K as _e,t as ke,aw as ot,ax as Gt,M as q,ay as je,x as E,az as Jt,O as Qt,R as me,P as Me,q as ea,B as ta,T as ht}from"./index-1b86b595.js";import{a as re,F as Ze,s as aa,r as nt,l as oa,b as na}from"./suno-e7ed7fd5.js";const la=oe([f("slider",`
 display: block;
 padding: calc((var(--n-handle-size) - var(--n-rail-height)) / 2) 0;
 position: relative;
 z-index: 0;
 width: 100%;
 cursor: pointer;
 user-select: none;
 -webkit-user-select: none;
 `,[C("reverse",[f("slider-handles",[f("slider-handle-wrapper",`
 transform: translate(50%, -50%);
 `)]),f("slider-dots",[f("slider-dot",`
 transform: translateX(50%, -50%);
 `)]),C("vertical",[f("slider-handles",[f("slider-handle-wrapper",`
 transform: translate(-50%, -50%);
 `)]),f("slider-marks",[f("slider-mark",`
 transform: translateY(calc(-50% + var(--n-dot-height) / 2));
 `)]),f("slider-dots",[f("slider-dot",`
 transform: translateX(-50%) translateY(0);
 `)])])]),C("vertical",`
 box-sizing: content-box;
 padding: 0 calc((var(--n-handle-size) - var(--n-rail-height)) / 2);
 width: var(--n-rail-width-vertical);
 height: 100%;
 `,[f("slider-handles",`
 top: calc(var(--n-handle-size) / 2);
 right: 0;
 bottom: calc(var(--n-handle-size) / 2);
 left: 0;
 `,[f("slider-handle-wrapper",`
 top: unset;
 left: 50%;
 transform: translate(-50%, 50%);
 `)]),f("slider-rail",`
 height: 100%;
 `,[k("fill",`
 top: unset;
 right: 0;
 bottom: unset;
 left: 0;
 `)]),C("with-mark",`
 width: var(--n-rail-width-vertical);
 margin: 0 32px 0 8px;
 `),f("slider-marks",`
 top: calc(var(--n-handle-size) / 2);
 right: unset;
 bottom: calc(var(--n-handle-size) / 2);
 left: 22px;
 font-size: var(--n-mark-font-size);
 `,[f("slider-mark",`
 transform: translateY(50%);
 white-space: nowrap;
 `)]),f("slider-dots",`
 top: calc(var(--n-handle-size) / 2);
 right: unset;
 bottom: calc(var(--n-handle-size) / 2);
 left: 50%;
 `,[f("slider-dot",`
 transform: translateX(-50%) translateY(50%);
 `)])]),C("disabled",`
 cursor: not-allowed;
 opacity: var(--n-opacity-disabled);
 `,[f("slider-handle",`
 cursor: not-allowed;
 `)]),C("with-mark",`
 width: 100%;
 margin: 8px 0 32px 0;
 `),oe("&:hover",[f("slider-rail",{backgroundColor:"var(--n-rail-color-hover)"},[k("fill",{backgroundColor:"var(--n-fill-color-hover)"})]),f("slider-handle",{boxShadow:"var(--n-handle-box-shadow-hover)"})]),C("active",[f("slider-rail",{backgroundColor:"var(--n-rail-color-hover)"},[k("fill",{backgroundColor:"var(--n-fill-color-hover)"})]),f("slider-handle",{boxShadow:"var(--n-handle-box-shadow-hover)"})]),f("slider-marks",`
 position: absolute;
 top: 18px;
 left: calc(var(--n-handle-size) / 2);
 right: calc(var(--n-handle-size) / 2);
 `,[f("slider-mark",`
 position: absolute;
 transform: translateX(-50%);
 white-space: nowrap;
 `)]),f("slider-rail",`
 width: 100%;
 position: relative;
 height: var(--n-rail-height);
 background-color: var(--n-rail-color);
 transition: background-color .3s var(--n-bezier);
 border-radius: calc(var(--n-rail-height) / 2);
 `,[k("fill",`
 position: absolute;
 top: 0;
 bottom: 0;
 border-radius: calc(var(--n-rail-height) / 2);
 transition: background-color .3s var(--n-bezier);
 background-color: var(--n-fill-color);
 `)]),f("slider-handles",`
 position: absolute;
 top: 0;
 right: calc(var(--n-handle-size) / 2);
 bottom: 0;
 left: calc(var(--n-handle-size) / 2);
 `,[f("slider-handle-wrapper",`
 outline: none;
 position: absolute;
 top: 50%;
 transform: translate(-50%, -50%);
 cursor: pointer;
 display: flex;
 `,[f("slider-handle",`
 height: var(--n-handle-size);
 width: var(--n-handle-size);
 border-radius: 50%;
 overflow: hidden;
 transition: box-shadow .2s var(--n-bezier), background-color .3s var(--n-bezier);
 background-color: var(--n-handle-color);
 box-shadow: var(--n-handle-box-shadow);
 `,[oe("&:hover",`
 box-shadow: var(--n-handle-box-shadow-hover);
 `)]),oe("&:focus",[f("slider-handle",`
 box-shadow: var(--n-handle-box-shadow-focus);
 `,[oe("&:hover",`
 box-shadow: var(--n-handle-box-shadow-active);
 `)])])])]),f("slider-dots",`
 position: absolute;
 top: 50%;
 left: calc(var(--n-handle-size) / 2);
 right: calc(var(--n-handle-size) / 2);
 `,[C("transition-disabled",[f("slider-dot","transition: none;")]),f("slider-dot",`
 transition:
 border-color .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 position: absolute;
 transform: translate(-50%, -50%);
 height: var(--n-dot-height);
 width: var(--n-dot-width);
 border-radius: var(--n-dot-border-radius);
 overflow: hidden;
 box-sizing: border-box;
 border: var(--n-dot-border);
 background-color: var(--n-dot-color);
 `,[C("active","border: var(--n-dot-border-active);")])])]),f("slider-handle-indicator",`
 font-size: var(--n-font-size);
 padding: 6px 10px;
 border-radius: var(--n-indicator-border-radius);
 color: var(--n-indicator-text-color);
 background-color: var(--n-indicator-color);
 box-shadow: var(--n-indicator-box-shadow);
 `,[Qe()]),f("slider-handle-indicator",`
 font-size: var(--n-font-size);
 padding: 6px 10px;
 border-radius: var(--n-indicator-border-radius);
 color: var(--n-indicator-text-color);
 background-color: var(--n-indicator-color);
 box-shadow: var(--n-indicator-box-shadow);
 `,[C("top",`
 margin-bottom: 12px;
 `),C("right",`
 margin-left: 12px;
 `),C("bottom",`
 margin-top: 12px;
 `),C("left",`
 margin-right: 12px;
 `),Qe()]),Mt(f("slider",[f("slider-dot","background-color: var(--n-dot-color-modal);")])),jt(f("slider",[f("slider-dot","background-color: var(--n-dot-color-popover);")]))]);function lt(e){return window.TouchEvent&&e instanceof window.TouchEvent}function st(){const e=new Map,n=d=>h=>{e.set(d,h)};return Ut(()=>{e.clear()}),[e,n]}const sa=0,ia=Object.assign(Object.assign({},Ue.props),{to:Ye.propTo,defaultValue:{type:[Number,Array],default:0},marks:Object,disabled:{type:Boolean,default:void 0},formatTooltip:Function,keyboard:{type:Boolean,default:!0},min:{type:Number,default:0},max:{type:Number,default:100},step:{type:[Number,String],default:1},range:Boolean,value:[Number,Array],placement:String,showTooltip:{type:Boolean,default:void 0},tooltip:{type:Boolean,default:!0},vertical:Boolean,reverse:Boolean,"onUpdate:value":[Function,Array],onUpdateValue:[Function,Array],onDragstart:[Function],onDragend:[Function]}),ft=ne({name:"Slider",props:ia,slots:Object,setup(e){const{mergedClsPrefixRef:n,namespaceRef:d,inlineThemeDisabled:h}=rt(e),l=Ue("Slider","-slider",la,Nt,e,n),p=D(null),[u,x]=st(),[F,j]=st(),L=D(new Set),B=dt(e),{mergedDisabledRef:r}=B,R=N(()=>{const{step:t}=e;if(Number(t)<=0||t==="mark")return 0;const a=t.toString();let s=0;return a.includes(".")&&(s=a.length-a.indexOf(".")-1),s}),o=D(e.defaultValue),c=ut(e,"value"),v=ct(c,o),V=N(()=>{const{value:t}=v;return(e.range?t:[t]).map(ee)}),W=N(()=>V.value.length>2),Z=N(()=>e.placement===void 0?e.vertical?"right":"top":e.placement),ze=N(()=>{const{marks:t}=e;return t?Object.keys(t).map(Number.parseFloat):null}),O=D(-1),be=D(-1),H=D(-1),_=D(!1),G=D(!1),Q=N(()=>{const{vertical:t,reverse:a}=e;return t?a?"top":"bottom":a?"right":"left"}),ue=N(()=>{if(W.value)return;const t=V.value,a=ce(e.range?Math.min(...t):e.min),s=ce(e.range?Math.max(...t):t[0]),{value:b}=Q;return e.vertical?{[b]:`${a}%`,height:`${s-a}%`}:{[b]:`${a}%`,width:`${s-a}%`}}),ge=N(()=>{const t=[],{marks:a}=e;if(a){const s=V.value.slice();s.sort((I,U)=>I-U);const{value:b}=Q,{value:S}=W,{range:M}=e,Y=S?()=>!1:I=>M?I>=s[0]&&I<=s[s.length-1]:I<=s[0];for(const I of Object.keys(a)){const U=Number(I);t.push({active:Y(U),key:U,label:a[I],style:{[b]:`${ce(U)}%`}})}}return t});function ye(t,a){const s=ce(t),{value:b}=Q;return{[b]:`${s}%`,zIndex:a===O.value?1:0}}function Se(t){return e.showTooltip||H.value===t||O.value===t&&_.value}function Ne(t){return _.value?!(O.value===t&&be.value===t):!0}function Ie(t){var a;~t&&(O.value=t,(a=u.get(t))===null||a===void 0||a.focus())}function Pe(){F.forEach((t,a)=>{Se(a)&&t.syncPosition()})}function X(t){const{"onUpdate:value":a,onUpdateValue:s}=e,{nTriggerFormInput:b,nTriggerFormChange:S}=B;s&&ie(s,t),a&&ie(a,t),o.value=t,b(),S()}function Re(t){const{range:a}=e;if(a){if(Array.isArray(t)){const{value:s}=V;t.join()!==s.join()&&X(t)}}else Array.isArray(t)||V.value[0]!==t&&X(t)}function xe(t,a){if(e.range){const s=V.value.slice();s.splice(a,1,t),Re(s)}else Re(t)}function K(t,a,s){const b=s!==void 0;s||(s=t-a>0?1:-1);const S=ze.value||[],{step:M}=e;if(M==="mark"){const U=te(t,S.concat(a),b?s:void 0);return U?U.value:a}if(M<=0)return a;const{value:Y}=R;let I;if(b){const U=Number((a/M).toFixed(Y)),ae=Math.floor(U),Ae=U>ae?ae:ae-1,Le=U<ae?ae:ae+1;I=te(a,[Number((Ae*M).toFixed(Y)),Number((Le*M).toFixed(Y)),...S],s)}else{const U=He(t);I=te(t,[...S,U])}return I?ee(I.value):a}function ee(t){return Math.min(e.max,Math.max(e.min,t))}function ce(t){const{max:a,min:s}=e;return(t-s)/(a-s)*100}function Ee(t){const{max:a,min:s}=e;return s+(a-s)*t}function He(t){const{step:a,min:s}=e;if(Number(a)<=0||a==="mark")return t;const b=Math.round((t-s)/a)*a+s;return Number(b.toFixed(R.value))}function te(t,a=ze.value,s){if(!(a!=null&&a.length))return null;let b=null,S=-1;for(;++S<a.length;){const M=a[S]-t,Y=Math.abs(M);(s===void 0||M*s>0)&&(b===null||Y<b.distance)&&(b={index:S,distance:Y,value:a[S]})}return b}function ve(t){const a=p.value;if(!a)return;const s=lt(t)?t.touches[0]:t,b=a.getBoundingClientRect();let S;return e.vertical?S=(b.bottom-s.clientY)/b.height:S=(s.clientX-b.left)/b.width,e.reverse&&(S=1-S),Ee(S)}function we(t){if(r.value||!e.keyboard)return;const{vertical:a,reverse:s}=e;switch(t.key){case"ArrowUp":t.preventDefault(),Ce(a&&s?-1:1);break;case"ArrowRight":t.preventDefault(),Ce(!a&&s?-1:1);break;case"ArrowDown":t.preventDefault(),Ce(a&&s?1:-1);break;case"ArrowLeft":t.preventDefault(),Ce(!a&&s?1:-1);break}}function Ce(t){const a=O.value;if(a===-1)return;const{step:s}=e,b=V.value[a],S=Number(s)<=0||s==="mark"?b:b+s*t;xe(K(S,b,t>0?1:-1),a)}function pt(t){var a,s;if(r.value||!lt(t)&&t.button!==sa)return;const b=ve(t);if(b===void 0)return;const S=V.value.slice(),M=e.range?(s=(a=te(b,S))===null||a===void 0?void 0:a.index)!==null&&s!==void 0?s:-1:0;M!==-1&&(t.preventDefault(),Ie(M),mt(),xe(K(b,V.value[M]),M))}function mt(){_.value||(_.value=!0,e.onDragstart&&ie(e.onDragstart),Fe("touchend",document,Ve),Fe("mouseup",document,Ve),Fe("touchmove",document,Te),Fe("mousemove",document,Te))}function De(){_.value&&(_.value=!1,e.onDragend&&ie(e.onDragend),Be("touchend",document,Ve),Be("mouseup",document,Ve),Be("touchmove",document,Te),Be("mousemove",document,Te))}function Te(t){const{value:a}=O;if(!_.value||a===-1){De();return}const s=ve(t);s!==void 0&&xe(K(s,V.value[a]),a)}function Ve(){De()}function bt(t){O.value=t,r.value||(H.value=t)}function gt(t){O.value===t&&(O.value=-1,De()),H.value===t&&(H.value=-1)}function yt(t){H.value=t}function xt(t){H.value===t&&(H.value=-1)}de(O,(t,a)=>void Oe(()=>be.value=a)),de(v,()=>{if(e.marks){if(G.value)return;G.value=!0,Oe(()=>{G.value=!1})}Oe(Pe)}),It(()=>{De()});const Ge=N(()=>{const{self:{markFontSize:t,railColor:a,railColorHover:s,fillColor:b,fillColorHover:S,handleColor:M,opacityDisabled:Y,dotColor:I,dotColorModal:U,handleBoxShadow:ae,handleBoxShadowHover:Ae,handleBoxShadowActive:Le,handleBoxShadowFocus:wt,dotBorder:_t,dotBoxShadow:kt,railHeight:$t,railWidthVertical:zt,handleSize:St,dotHeight:Rt,dotWidth:Ct,dotBorderRadius:Dt,fontSize:Tt,dotBorderActive:Vt,dotColorPopover:Ft},common:{cubicBezierEaseInOut:Bt}}=l.value;return{"--n-bezier":Bt,"--n-dot-border":_t,"--n-dot-border-active":Vt,"--n-dot-border-radius":Dt,"--n-dot-box-shadow":kt,"--n-dot-color":I,"--n-dot-color-modal":U,"--n-dot-color-popover":Ft,"--n-dot-height":Rt,"--n-dot-width":Ct,"--n-fill-color":b,"--n-fill-color-hover":S,"--n-font-size":Tt,"--n-handle-box-shadow":ae,"--n-handle-box-shadow-active":Le,"--n-handle-box-shadow-focus":wt,"--n-handle-box-shadow-hover":Ae,"--n-handle-color":M,"--n-handle-size":St,"--n-opacity-disabled":Y,"--n-rail-color":a,"--n-rail-color-hover":s,"--n-rail-height":$t,"--n-rail-width-vertical":zt,"--n-mark-font-size":t}}),he=h?Xe("slider",void 0,Ge,e):void 0,Je=N(()=>{const{self:{fontSize:t,indicatorColor:a,indicatorBoxShadow:s,indicatorTextColor:b,indicatorBorderRadius:S}}=l.value;return{"--n-font-size":t,"--n-indicator-border-radius":S,"--n-indicator-box-shadow":s,"--n-indicator-color":a,"--n-indicator-text-color":b}}),fe=h?Xe("slider-indicator",void 0,Je,e):void 0;return{mergedClsPrefix:n,namespace:d,uncontrolledValue:o,mergedValue:v,mergedDisabled:r,mergedPlacement:Z,isMounted:Pt(),adjustedTo:Ye(e),dotTransitionDisabled:G,markInfos:ge,isShowTooltip:Se,shouldKeepTooltipTransition:Ne,handleRailRef:p,setHandleRefs:x,setFollowerRefs:j,fillStyle:ue,getHandleStyle:ye,activeIndex:O,arrifiedValues:V,followerEnabledIndexSet:L,handleRailMouseDown:pt,handleHandleFocus:bt,handleHandleBlur:gt,handleHandleMouseEnter:yt,handleHandleMouseLeave:xt,handleRailKeyDown:we,indicatorCssVars:h?void 0:Je,indicatorThemeClass:fe==null?void 0:fe.themeClass,indicatorOnRender:fe==null?void 0:fe.onRender,cssVars:h?void 0:Ge,themeClass:he==null?void 0:he.themeClass,onRender:he==null?void 0:he.onRender}},render(){var e;const{mergedClsPrefix:n,themeClass:d,formatTooltip:h}=this;return(e=this.onRender)===null||e===void 0||e.call(this),$("div",{class:[`${n}-slider`,d,{[`${n}-slider--disabled`]:this.mergedDisabled,[`${n}-slider--active`]:this.activeIndex!==-1,[`${n}-slider--with-mark`]:this.marks,[`${n}-slider--vertical`]:this.vertical,[`${n}-slider--reverse`]:this.reverse}],style:this.cssVars,onKeydown:this.handleRailKeyDown,onMousedown:this.handleRailMouseDown,onTouchstart:this.handleRailMouseDown},$("div",{class:`${n}-slider-rail`},$("div",{class:`${n}-slider-rail__fill`,style:this.fillStyle}),this.marks?$("div",{class:[`${n}-slider-dots`,this.dotTransitionDisabled&&`${n}-slider-dots--transition-disabled`]},this.markInfos.map(l=>$("div",{key:l.key,class:[`${n}-slider-dot`,{[`${n}-slider-dot--active`]:l.active}],style:l.style}))):null,$("div",{ref:"handleRailRef",class:`${n}-slider-handles`},this.arrifiedValues.map((l,p)=>{const u=this.isShowTooltip(p);return $(Et,null,{default:()=>[$(Ht,null,{default:()=>$("div",{ref:this.setHandleRefs(p),class:`${n}-slider-handle-wrapper`,tabindex:this.mergedDisabled?-1:0,role:"slider","aria-valuenow":l,"aria-valuemin":this.min,"aria-valuemax":this.max,"aria-orientation":this.vertical?"vertical":"horizontal","aria-disabled":this.disabled,style:this.getHandleStyle(l,p),onFocus:()=>{this.handleHandleFocus(p)},onBlur:()=>{this.handleHandleBlur(p)},onMouseenter:()=>{this.handleHandleMouseEnter(p)},onMouseleave:()=>{this.handleHandleMouseLeave(p)}},At(this.$slots.thumb,()=>[$("div",{class:`${n}-slider-handle`})]))}),this.tooltip&&$(Lt,{ref:this.setFollowerRefs(p),show:u,to:this.adjustedTo,enabled:this.showTooltip&&!this.range||this.followerEnabledIndexSet.has(p),teleportDisabled:this.adjustedTo===Ye.tdkey,placement:this.mergedPlacement,containerClass:this.namespace},{default:()=>$(Ot,{name:"fade-in-scale-up-transition",appear:this.isMounted,css:this.shouldKeepTooltipTransition(p),onEnter:()=>{this.followerEnabledIndexSet.add(p)},onAfterLeave:()=>{this.followerEnabledIndexSet.delete(p)}},{default:()=>{var x;return u?((x=this.indicatorOnRender)===null||x===void 0||x.call(this),$("div",{class:[`${n}-slider-handle-indicator`,this.indicatorThemeClass,`${n}-slider-handle-indicator--${this.mergedPlacement}`],style:this.indicatorCssVars},typeof h=="function"?h(l):l)):null}})})]})})),this.marks?$("div",{class:`${n}-slider-marks`},this.markInfos.map(l=>$("div",{key:l.key,class:`${n}-slider-mark`,style:l.style},typeof l.label=="function"?l.label():l.label))):null))}}),ra=f("switch",`
 height: var(--n-height);
 min-width: var(--n-width);
 vertical-align: middle;
 user-select: none;
 -webkit-user-select: none;
 display: inline-flex;
 outline: none;
 justify-content: center;
 align-items: center;
`,[k("children-placeholder",`
 height: var(--n-rail-height);
 display: flex;
 flex-direction: column;
 overflow: hidden;
 pointer-events: none;
 visibility: hidden;
 `),k("rail-placeholder",`
 display: flex;
 flex-wrap: none;
 `),k("button-placeholder",`
 width: calc(1.75 * var(--n-rail-height));
 height: var(--n-rail-height);
 `),f("base-loading",`
 position: absolute;
 top: 50%;
 left: 50%;
 transform: translateX(-50%) translateY(-50%);
 font-size: calc(var(--n-button-width) - 4px);
 color: var(--n-loading-color);
 transition: color .3s var(--n-bezier);
 `,[et({left:"50%",top:"50%",originalTransform:"translateX(-50%) translateY(-50%)"})]),k("checked, unchecked",`
 transition: color .3s var(--n-bezier);
 color: var(--n-text-color);
 box-sizing: border-box;
 position: absolute;
 white-space: nowrap;
 top: 0;
 bottom: 0;
 display: flex;
 align-items: center;
 line-height: 1;
 `),k("checked",`
 right: 0;
 padding-right: calc(1.25 * var(--n-rail-height) - var(--n-offset));
 `),k("unchecked",`
 left: 0;
 justify-content: flex-end;
 padding-left: calc(1.25 * var(--n-rail-height) - var(--n-offset));
 `),oe("&:focus",[k("rail",`
 box-shadow: var(--n-box-shadow-focus);
 `)]),C("round",[k("rail","border-radius: calc(var(--n-rail-height) / 2);",[k("button","border-radius: calc(var(--n-button-height) / 2);")])]),tt("disabled",[tt("icon",[C("rubber-band",[C("pressed",[k("rail",[k("button","max-width: var(--n-button-width-pressed);")])]),k("rail",[oe("&:active",[k("button","max-width: var(--n-button-width-pressed);")])]),C("active",[C("pressed",[k("rail",[k("button","left: calc(100% - var(--n-offset) - var(--n-button-width-pressed));")])]),k("rail",[oe("&:active",[k("button","left: calc(100% - var(--n-offset) - var(--n-button-width-pressed));")])])])])])]),C("active",[k("rail",[k("button","left: calc(100% - var(--n-button-width) - var(--n-offset))")])]),k("rail",`
 overflow: hidden;
 height: var(--n-rail-height);
 min-width: var(--n-rail-width);
 border-radius: var(--n-rail-border-radius);
 cursor: pointer;
 position: relative;
 transition:
 opacity .3s var(--n-bezier),
 background .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier);
 background-color: var(--n-rail-color);
 `,[k("button-icon",`
 color: var(--n-icon-color);
 transition: color .3s var(--n-bezier);
 font-size: calc(var(--n-button-height) - 4px);
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 display: flex;
 justify-content: center;
 align-items: center;
 line-height: 1;
 `,[et()]),k("button",`
 align-items: center; 
 top: var(--n-offset);
 left: var(--n-offset);
 height: var(--n-button-height);
 width: var(--n-button-width-pressed);
 max-width: var(--n-button-width);
 border-radius: var(--n-button-border-radius);
 background-color: var(--n-button-color);
 box-shadow: var(--n-button-box-shadow);
 box-sizing: border-box;
 cursor: inherit;
 content: "";
 position: absolute;
 transition:
 background-color .3s var(--n-bezier),
 left .3s var(--n-bezier),
 opacity .3s var(--n-bezier),
 max-width .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier);
 `)]),C("active",[k("rail","background-color: var(--n-rail-color-active);")]),C("loading",[k("rail",`
 cursor: wait;
 `)]),C("disabled",[k("rail",`
 cursor: not-allowed;
 opacity: .5;
 `)])]),da=Object.assign(Object.assign({},Ue.props),{size:{type:String,default:"medium"},value:{type:[String,Number,Boolean],default:void 0},loading:Boolean,defaultValue:{type:[String,Number,Boolean],default:!1},disabled:{type:Boolean,default:void 0},round:{type:Boolean,default:!0},"onUpdate:value":[Function,Array],onUpdateValue:[Function,Array],checkedValue:{type:[String,Number,Boolean],default:!0},uncheckedValue:{type:[String,Number,Boolean],default:!1},railStyle:Function,rubberBand:{type:Boolean,default:!0},onChange:[Function,Array]});let $e;const it=ne({name:"Switch",props:da,slots:Object,setup(e){$e===void 0&&(typeof CSS<"u"?typeof CSS.supports<"u"?$e=CSS.supports("width","max(1px)"):$e=!1:$e=!0);const{mergedClsPrefixRef:n,inlineThemeDisabled:d}=rt(e),h=Ue("Switch","-switch",ra,Kt,e,n),l=dt(e),{mergedSizeRef:p,mergedDisabledRef:u}=l,x=D(e.defaultValue),F=ut(e,"value"),j=ct(F,x),L=N(()=>j.value===e.checkedValue),B=D(!1),r=D(!1),R=N(()=>{const{railStyle:_}=e;if(_)return _({focused:r.value,checked:L.value})});function o(_){const{"onUpdate:value":G,onChange:Q,onUpdateValue:ue}=e,{nTriggerFormInput:ge,nTriggerFormChange:ye}=l;G&&ie(G,_),ue&&ie(ue,_),Q&&ie(Q,_),x.value=_,ge(),ye()}function c(){const{nTriggerFormFocus:_}=l;_()}function v(){const{nTriggerFormBlur:_}=l;_()}function V(){e.loading||u.value||(j.value!==e.checkedValue?o(e.checkedValue):o(e.uncheckedValue))}function W(){r.value=!0,c()}function Z(){r.value=!1,v(),B.value=!1}function ze(_){e.loading||u.value||_.key===" "&&(j.value!==e.checkedValue?o(e.checkedValue):o(e.uncheckedValue),B.value=!1)}function O(_){e.loading||u.value||_.key===" "&&(_.preventDefault(),B.value=!0)}const be=N(()=>{const{value:_}=p,{self:{opacityDisabled:G,railColor:Q,railColorActive:ue,buttonBoxShadow:ge,buttonColor:ye,boxShadowFocus:Se,loadingColor:Ne,textColor:Ie,iconColor:Pe,[le("buttonHeight",_)]:X,[le("buttonWidth",_)]:Re,[le("buttonWidthPressed",_)]:xe,[le("railHeight",_)]:K,[le("railWidth",_)]:ee,[le("railBorderRadius",_)]:ce,[le("buttonBorderRadius",_)]:Ee},common:{cubicBezierEaseInOut:He}}=h.value;let te,ve,we;return $e?(te=`calc((${K} - ${X}) / 2)`,ve=`max(${K}, ${X})`,we=`max(${ee}, calc(${ee} + ${X} - ${K}))`):(te=Ke((J(K)-J(X))/2),ve=Ke(Math.max(J(K),J(X))),we=J(K)>J(X)?ee:Ke(J(ee)+J(X)-J(K))),{"--n-bezier":He,"--n-button-border-radius":Ee,"--n-button-box-shadow":ge,"--n-button-color":ye,"--n-button-width":Re,"--n-button-width-pressed":xe,"--n-button-height":X,"--n-height":ve,"--n-offset":te,"--n-opacity-disabled":G,"--n-rail-border-radius":ce,"--n-rail-color":Q,"--n-rail-color-active":ue,"--n-rail-height":K,"--n-rail-width":ee,"--n-width":we,"--n-box-shadow-focus":Se,"--n-loading-color":Ne,"--n-text-color":Ie,"--n-icon-color":Pe}}),H=d?Xe("switch",N(()=>p.value[0]),be,e):void 0;return{handleClick:V,handleBlur:Z,handleFocus:W,handleKeyup:ze,handleKeydown:O,mergedRailStyle:R,pressed:B,mergedClsPrefix:n,mergedValue:j,checked:L,mergedDisabled:u,cssVars:d?void 0:be,themeClass:H==null?void 0:H.themeClass,onRender:H==null?void 0:H.onRender}},render(){const{mergedClsPrefix:e,mergedDisabled:n,checked:d,mergedRailStyle:h,onRender:l,$slots:p}=this;l==null||l();const{checked:u,unchecked:x,icon:F,"checked-icon":j,"unchecked-icon":L}=p,B=!(We(F)&&We(j)&&We(L));return $("div",{role:"switch","aria-checked":d,class:[`${e}-switch`,this.themeClass,B&&`${e}-switch--icon`,d&&`${e}-switch--active`,n&&`${e}-switch--disabled`,this.round&&`${e}-switch--round`,this.loading&&`${e}-switch--loading`,this.pressed&&`${e}-switch--pressed`,this.rubberBand&&`${e}-switch--rubber-band`],tabindex:this.mergedDisabled?void 0:0,style:this.cssVars,onClick:this.handleClick,onFocus:this.handleFocus,onBlur:this.handleBlur,onKeyup:this.handleKeyup,onKeydown:this.handleKeydown},$("div",{class:`${e}-switch__rail`,"aria-hidden":"true",style:h},se(u,r=>se(x,R=>r||R?$("div",{"aria-hidden":!0,class:`${e}-switch__children-placeholder`},$("div",{class:`${e}-switch__rail-placeholder`},$("div",{class:`${e}-switch__button-placeholder`}),r),$("div",{class:`${e}-switch__rail-placeholder`},$("div",{class:`${e}-switch__button-placeholder`}),R)):null)),$("div",{class:`${e}-switch__button`},se(F,r=>se(j,R=>se(L,o=>$(Wt,null,{default:()=>this.loading?$(Xt,{key:"loading",clsPrefix:e,strokeWidth:20}):this.checked&&(R||r)?$("div",{class:`${e}-switch__button-icon`,key:R?"checked-icon":"icon"},R||r):!this.checked&&(o||r)?$("div",{class:`${e}-switch__button-icon`,key:o?"unchecked-icon":"icon"},o||r):null})))),se(u,r=>r&&$("div",{key:"checked",class:`${e}-switch__checked`},r)),se(x,r=>r&&$("div",{key:"unchecked",class:`${e}-switch__unchecked`},r)))))}}),ua={key:0,class:"cursor-pointer"},ca=ne({__name:"mcUploadMp3",setup(e){const n=D(),d=D({process:"",id:"",isUpload:!1}),h=async p=>{for(let u=0;u<50;u++){let x=await re(`/uploads/audio/${p}`);P("ddd",x);let F=u+1;if(F>20&&(F=20),x.status=="complete"||x.status=="error")return x;await aa(F*1e3)}return null};async function l(p){try{d.value.isUpload=!0,P("uploadFile",p.target.files[0]);const u=await re("/uploads/audio",{extension:"mp3"});P("init ",u),d.value.id=u.id;const x=new FormData;for(let r in u.fields)x.append(r,u.fields[r]);if(x.append("file",p.target.files[0]),!(await fetch(u.url,{method:"POST",body:x})).ok)throw new Error("Network response was not ok");P("uploaded ");const j=await re("/uploads/audio/"+u.id+"/upload-finish",{upload_type:"file_upload",upload_filename:p.target.files[0].name});P("finish ",j);const L=await h(u.id);P("uploadFetch ",L);const B=await re("/uploads/audio/"+u.id+"/initialize-clip",{});P("clip ",B),Ze([B.clip_id])}catch{}d.value.isUpload=!1,n.value.value=""}return(p,u)=>(y(),z(pe,null,[w(m(qe),{type:"info",size:"small",round:"",bordered:!1},{default:T(()=>[d.value.isUpload?(y(),z("span",ua,"Upload...")):(y(),z("span",{key:1,class:"cursor-pointer",onClick:u[0]||(u[0]=x=>n.value.click())},g(p.$t("suno.upMps")),1))]),_:1}),i("input",{type:"file",onChange:l,ref_key:"fsRef",ref:n,style:{display:"none"},accept:".mp3"},null,544)],64))}}),va={class:"p-2"},ha={class:"pt-1"},fa={class:"pt-4 flex justify-between",style:{"margin-bottom":"10px"}},pa={class:"pt-1"},ma={class:"pt-1"},ba={class:"pt-1"},ga={class:"pt-4"},ya={class:"pt-4 flex justify-between",style:{"margin-bottom":"15px"}},xa={class:"pt-1"},wa={class:"pt-1"},_a={class:"pt-5"},ka={class:"flex justify-between pb-3"},$a={class:"text-[12px]"},za={class:"bg-[--n-fill-color] text-[9px] border-[0px] px-1 list-none rounded-md"},Sa={class:"pt-1"},Ra={class:"flex relative justify-between items-start p-2 hover:dark:bg-black hover:bg-gray-200 border-b-[1px] border-gray-500/10"},Ca={class:"w-[60px] h-[60px] relative cursor-pointer"},Da={class:"w-full h-full justify-center items-center flex"},Ta={class:"flex-1 pl-2"},Va={class:"flex justify-between line-clamp-1 w-full cursor-pointer"},Fa={key:0,class:"opacity-60 line-clamp-1 w-full text-[12px] cursor-pointer"},Ba={key:1,class:"opacity-60 line-clamp-1 w-full text-[12px] cursor-pointer"},Ma={class:"text-right text-[14px] flex justify-end items-center space-x-2"},ja={key:0,class:"text-[8px] flex items-center border-[1px] border-red-500/80 px-1 list-none rounded-md"},Ua={key:1,class:"text-[8px] flex items-center border-[1px] border-gray-500/30 px-1 list-none rounded-md"},Na={key:2,class:"text-[8px] flex items-center border-[1px] border-gray-500/30 px-1 list-none rounded-md"},Ia={class:"pt-4"},Pa={class:"flex justify-between items-start"},Ea={class:"flex items-start",style:{"margin-top":"15px"}},Ha=["innerHTML"],Aa=ne({__name:"mcInput",setup(e){const n=D({type:"custom",isLoading:!1}),d=D(),h=D({gpt_description_prompt:"",make_instrumental:!1,mv:"chirp-v3-5",prompt:""}),l=D({prompt:"",mv:"chirp-v3-5",title:"",tags:"",continue_at:120,continue_clip_id:""}),p=Yt(),u=[{label:"verion: v3.5",value:"chirp-v3-5"},{label:"verion: v3",value:"chirp-v3-0"}],x=N(()=>n.value.isLoading?!1:n.value.type=="custom"?l.value.tags&&l.value.title:n.value.type=="description"?(P("des: ",h.value.gpt_description_prompt,h.value.make_instrumental),l.value.title&&(h.value.gpt_description_prompt||h.value.make_instrumental)):!0),F=vt();qt(()=>{A.setMyData({ms:F})});const j=()=>{let o=l.value.prompt||l.value.title;if(!o){F.error(Me("suno.inputly"));return}if(n.value.isLoading){F.info(Me("suno.doingly"));return}n.value.isLoading=!0,F.info(Me("suno.doingly2")),re("/generate/lyrics/",{prompt:o}).then(async c=>{P("lyrics",c);let v=await oa(c.data);P("lyrics rz =>",v),v!=null&&(l.value.prompt=v.data.data.text,l.value.title=v.data.data.title),n.value.isLoading=!1}).catch(()=>n.value.isLoading=!1),l.value.tags||(l.value.tags=nt())},L=async()=>{var c,v;n.value.isLoading=!1;let o=["0d435185-d440-42c8-982a-50205e1cf17d","43e095ba-5f08-4920-bb3d-89dd0defe0b7"];if(o=["d359a0aa-adf1-4298-9074-005573d7cc84","12e3d62f-8fcc-497b-8365-194657582519"],n.value.type=="custom"){h.value.make_instrumental&&(l.value.prompt=""),l.value.continue_clip_id!=""&&((v=(c=d.value)==null?void 0:c.metadata)==null?void 0:v.type)=="upload"&&(l.value.mv="chirp-v3-5-upload");let V=await re("/generate",l.value);n.value.isLoading=!1,o=V.clips.map(W=>W.id),P("ids ",o),(l.value.mv="chirp-v3-5-upload")&&(l.value.mv="chirp-v3-5")}else{h.value.prompt=l.value.title;let V=await re("/generate/description-mode",h.value);n.value.isLoading=!1,o=V.clips.map(W=>W.id)}Ze(o)};de(()=>A.myData.act,o=>{if(o=="suno.extend"){P("suno.extend",A.myData.actData);const c=A.myData.actData;d.value=c,l.value.continue_clip_id=c.id,l.value.continue_at=Math.ceil(c.metadata.duration/2)}});const B=Zt(),r=N(()=>B.theme==="auto"?p.value==="dark":B.theme==="dark"),R=({focused:o,checked:c})=>{const v={};return c&&(v.background="#0084FF"),v};return(o,c)=>(y(),z("div",va,[w(m(Jt),{type:"line",animated:"",value:n.value.type,"onUpdate:value":c[12]||(c[12]=v=>n.value.type=v)},{default:T(()=>[w(m(at),{name:"description",tab:o.$t("suno.description")},{default:T(()=>[i("div",ha,[w(m(_e),{placeholder:o.$t("suno.titlepls"),value:l.value.title,"onUpdate:value":c[0]||(c[0]=v=>l.value.title=v)},{prefix:T(()=>[i("span",null,g(o.$t("suno.title"))+"：",1)]),_:1},8,["placeholder","value"])]),i("div",fa,[i("div",null,g(o.$t("suno.desc"))+":",1),i("div",null,[w(m(it),{value:h.value.make_instrumental,"onUpdate:value":c[1]||(c[1]=v=>h.value.make_instrumental=v),size:"small","rail-style":r.value?R:""},{checked:T(()=>[ke(g(o.$t("suno.noneedly")),1)]),unchecked:T(()=>[ke(g(o.$t("suno.noneedly")),1)]),_:1},8,["value","rail-style"])])]),i("div",pa,[w(m(_e),{value:h.value.gpt_description_prompt,"onUpdate:value":c[2]||(c[2]=v=>h.value.gpt_description_prompt=v),disabled:h.value.make_instrumental,placeholder:o.$t("suno.descpls"),type:"textarea",size:"small",autosize:{minRows:3,maxRows:12}},null,8,["value","disabled","placeholder"])]),i("div",ma,[w(m(ot),{value:h.value.mv,"onUpdate:value":c[3]||(c[3]=v=>h.value.mv=v),options:u,size:"small"},null,8,["value"])])]),_:1},8,["tab"]),w(m(at),{name:"custom",tab:o.$t("suno.custom")},{default:T(()=>[i("div",ba,[w(m(_e),{placeholder:o.$t("suno.titlepls"),value:l.value.title,"onUpdate:value":c[4]||(c[4]=v=>l.value.title=v)},{prefix:T(()=>[i("span",null,g(o.$t("suno.title"))+"：",1)]),_:1},8,["placeholder","value"])]),i("div",ga,[w(m(_e),{placeholder:o.$t("suno.stylepls"),value:l.value.tags,"onUpdate:value":c[6]||(c[6]=v=>l.value.tags=v)},{prefix:T(()=>[i("span",null,g(o.$t("suno.style"))+"：",1)]),suffix:T(()=>[w(m(Gt),{placement:"right",trigger:"hover"},{trigger:T(()=>[i("div",{class:"cursor-pointer",onClick:c[5]||(c[5]=v=>l.value.tags=m(nt)())},[w(m(q),{icon:"fa:random",class:"w-4 h-4"})])]),default:T(()=>[i("div",null,g(o.$t("suno.rank")),1)]),_:1})]),_:1},8,["placeholder","value"])]),i("div",ya,[i("div",null,g(o.$t("suno.ly"))+" :",1),i("div",null,[w(m(it),{value:h.value.make_instrumental,"onUpdate:value":c[7]||(c[7]=v=>h.value.make_instrumental=v),size:"small","rail-style":r.value?R:""},{checked:T(()=>[ke(g(o.$t("suno.noneedly")),1)]),unchecked:T(()=>[ke(g(o.$t("suno.noneedly")),1)]),_:1},8,["value","rail-style"])])]),i("div",xa,[w(m(_e),{value:l.value.prompt,"onUpdate:value":c[8]||(c[8]=v=>l.value.prompt=v),disabled:h.value.make_instrumental,placeholder:o.$t("suno.lypls"),type:"textarea",size:"small",autosize:{minRows:3,maxRows:12}},null,8,["value","disabled","placeholder"])]),i("div",wa,[w(m(ot),{value:l.value.mv,"onUpdate:value":c[9]||(c[9]=v=>l.value.mv=v),options:u,size:"small"},null,8,["value"])]),l.value.continue_clip_id&&d.value?(y(),z(pe,{key:0},[i("div",_a,[i("div",ka,[i("div",$a,g(o.$t("suno.extendAt"))+" "+g(l.value.continue_at)+"s",1),w(m(qe),{type:"success",size:"small",round:""},{default:T(()=>[i("span",{class:"cursor-pointer",onClick:c[10]||(c[10]=v=>l.value.continue_clip_id="")},"清除")]),_:1})]),w(m(ft),{value:l.value.continue_at,"onUpdate:value":c[11]||(c[11]=v=>l.value.continue_at=v),step:1,max:Math.ceil(d.value.metadata.duration)},{thumb:T(()=>[i("div",za,g(l.value.continue_at)+"s",1)]),_:1},8,["value","max"])]),i("div",Sa,[i("div",Ra,[i("div",Ca,[w(m(je),{lazy:"",width:"100",src:d.value.image_url,"preview-disabled":""},{placeholder:T(()=>[i("div",Da,[w(m(q),{icon:"line-md:downloading-loop",class:"text-[40px] text-green-300"})])]),_:1},8,["src"])]),i("div",Ta,[i("div",Va,[i("h3",null,g(d.value.title),1)]),d.value.metadata&&d.value.metadata.prompt?(y(),z("div",Fa,g(d.value.metadata.prompt),1)):(y(),z("div",Ba,g(o.$t("suno.noly")),1)),i("div",Ma,[d.value.status=="error"?(y(),z("div",ja,"失败")):E("",!0),d.value.metadata&&d.value.metadata.duration?(y(),z("div",Ua,g(d.value.metadata.duration.toFixed(1))+"s",1)):E("",!0),d.value.major_model_version?(y(),z("div",Na,g(d.value.major_model_version),1)):E("",!0)])])])])],64)):E("",!0)]),_:1},8,["tab"])]),_:1},8,["value"]),i("div",Ia,[i("div",Pa,[w(m(Qt),{type:"success",class:"genner-button",bordered:!1,style:{"border-radius":"8px"},disabled:!x.value,onClick:c[13]||(c[13]=v=>L())},{default:T(()=>[w(m(q),{icon:"ri:music-fill"}),ke(" "+g(o.$t("suno.generate")),1)]),_:1},8,["disabled"])]),i("div",Ea,[n.value.type=="custom"?(y(),me(m(qe),{key:0,type:"info",round:"",bordered:!1,style:{"margin-right":"15px"},size:"small"},{default:T(()=>[i("span",{class:"cursor-pointer",onClick:c[14]||(c[14]=v=>j())},g(o.$t("suno.generately")),1)]),_:1})):E("",!0),n.value.type=="custom"?(y(),me(ca,{key:1})):E("",!0)])]),n.value.type=="custom"?(y(),z("div",{key:0,style:{color:"#d84c10"},class:"pt-4 text-[12px]",innerHTML:m(Me)("suno.info")},null,8,Ha)):E("",!0)]))}}),La={class:"sss",style:{"--n-rail-height":"2px"}},Oa=ne({__name:"playui",emits:["update"],setup(e,{emit:n}){const d=D({v:10,max:0,status:"",idDrop:!1}),h=p=>{A.setMyData({act:"playUpdate",actData:{v:p}})},l=n;return de(()=>A.myData.act2,p=>{if(p=="playStatus"){if(d.value.idDrop)return;let u=A.myData.actData;P("playStatus",u),u&&u.d&&u.d.duration&&(d.value.max=u.d.duration,d.value.v=u.d.currentTime),u&&(d.value.status=u.a),l("update",d.value)}}),de(()=>A.myData.act,p=>{if(p=="playStatus"){let u=A.myData.actData;u&&(d.value.status=u.a),l("update",d.value)}}),(p,u)=>(y(),z("div",La,[d.value.max?(y(),me(m(ft),{key:0,"on-dragend":()=>d.value.idDrop=!1,"on-dragstart":()=>d.value.idDrop=!0,class:"w-full",value:d.value.v,"onUpdate:value":u[0]||(u[0]=x=>d.value.v=x),step:1,max:d.value.max,"on-update:value":h,"format-tooltip":x=>x.toFixed(1)+"s"},null,8,["on-dragend","on-dragstart","value","max","format-tooltip"])):E("",!0)]))}});const Ka={key:0},Wa=["onClick"],Xa={class:"w-full h-full justify-center items-center flex"},Ya={key:0,class:"absolute top-0 right-0 w-full h-full flex justify-center items-center"},qa={class:"absolute top-0 right-0 w-full h-full justify-center items-center flex"},Za={class:"flex-1 pl-2"},Ga=["onClick"],Ja={class:"flex justify-start items-center"},Qa={key:0,class:"text-[8px] flex items-center border-[1px] border-gray-500/30 px-1 ml-1 list-none rounded-md"},eo={class:"opacity-80"},to=["onClick"],ao=["onClick"],oo={class:"text-right text-[14px] flex justify-end items-center space-x-2"},no={key:0,class:"text-[8px] flex items-center border-[1px] border-gray-500/30 px-1 list-none rounded-md"},lo={key:1,class:"text-[8px] flex items-center border-[1px] border-red-500/80 px-1 list-none rounded-md"},so={class:"text-[8px] flex items-center border-[1px] border-gray-500/30 px-1 list-none rounded-md"},io=["onClick"],ro={key:3,class:"text-[8px] flex items-center border-[1px] border-gray-500/30 px-1 list-none rounded-md"},uo=["href"],co={key:1,class:"w-full h-full flex justify-center items-center"},vo=ne({__name:"mcList",setup(e){const n=D([]),d=new na,h=D({playid:""}),l=vt(),p=()=>{let r=d.getObjs();n.value=r.reverse()},u=r=>r.id==h.value.playid?["bg-gray-200","dark:bg-black"]:[],x=r=>{if(r.status=="error"){l.info("这首歌生成失败！");return}h.value.playid=r.id,A.setMyData({act:"goPlay",actData:r}),r.status!="complete"&&Ze([r.id])},F=r=>{P("extend",F),A.setMyData({act:"suno.extend",actData:r})},j=D({v:10,max:0,status:"",idDrop:!1});de(()=>A.myData.act,r=>{if(r=="FeedTask"&&p(),r=="playEned"){let R=n.value.findIndex(o=>o.id==h.value.playid);R++,P("playEned,",R,n.value.length),R<n.value.length&&setTimeout(()=>x(n.value[R]),1e3)}});const L=r=>{r=r.replace("m_","");let R=n.value.findIndex(o=>o.id==r);return R<0?null:n.value[R]},B=r=>{j.value=r};return p(),(r,R)=>n.value.length>0?(y(),z("div",Ka,[(y(!0),z(pe,null,ea(n.value,o=>{var c,v,V,W;return y(),z("div",{class:ta([u(o),"flex relative justify-between items-start p-2 hover:dark:bg-black hover:bg-gray-200 border-b-[1px] border-gray-500/10"])},[h.value.playid==o.id?(y(),me(Oa,{key:0,onUpdate:B,class:"absolute top-[-4px] left-0 w-full z-10"})):E("",!0),i("div",{class:"w-[60px] h-[60px] relative cursor-pointer",onClick:Z=>x(o)},[o.status=="complete"?(y(),z(pe,{key:0},[w(m(je),{lazy:"",width:"100",src:o.image_url,"preview-disabled":""},{placeholder:T(()=>[i("div",Xa,[w(m(q),{icon:"line-md:downloading-loop",class:"text-[40px] text-green-300"})])]),_:1},8,["src"]),h.value.playid==o.id?(y(),z("div",Ya,[j.value.status=="pause"?(y(),me(m(q),{key:0,icon:"mdi:pause-circle-outline",class:"text-[40px] text-[#fff]"})):(y(),me(m(q),{key:1,icon:"mdi:play-circle-outline",class:"text-[40px] text-[#fff]"}))])):E("",!0)],64)):(y(),z(pe,{key:1},[w(m(je),{lazy:"",width:"100",src:o.image_url,"preview-disabled":""},null,8,["src"]),i("div",qa,[w(m(q),{icon:"line-md:downloading-loop",class:"text-[40px] text-green-300"})])],64))],8,Wa),i("div",Za,[i("div",{class:"flex justify-between line-clamp-1 w-full cursor-pointer",onClick:Z=>x(o)},[i("div",Ja,[i("h3",null,g(o.title),1),((c=o.metadata)==null?void 0:c.type)=="upload"?(y(),z("div",Qa,"Uploaded")):E("",!0)]),i("div",eo,g(o.metadata.tags),1)],8,Ga),o.metadata&&o.metadata.prompt?(y(),z("div",{key:0,class:"opacity-60 line-clamp-1 w-full text-[12px] cursor-pointer",onClick:Z=>x(o)},g(o.metadata.prompt),9,to)):(y(),z("div",{key:1,class:"opacity-60 line-clamp-1 w-full text-[12px] cursor-pointer",onClick:Z=>x(o)},g(r.$t("suno.noly")),9,ao)),i("div",oo,[(v=o.metadata)!=null&&v.audio_prompt_id?(y(),z("div",no,g(r.$t("suno.extendFrom"))+":"+g((W=L((V=o.metadata)==null?void 0:V.audio_prompt_id))==null?void 0:W.title),1)):E("",!0),o.status=="error"?(y(),z("div",lo,g(r.$t("suno.fail")),1)):E("",!0),o.metadata&&o.metadata.duration?(y(),z(pe,{key:2},[i("div",so,g(o.metadata.duration.toFixed(1))+"s",1),i("div",{onClick:Z=>F(o),class:"text-[8px] flex items-center border-[1px] border-gray-500/30 px-1 list-none rounded-md cursor-pointer"},g(r.$t("suno.extend")),9,io)],64)):E("",!0),o.major_model_version?(y(),z("div",ro,g(o.major_model_version),1)):E("",!0),w(m(q),{icon:"mdi:play-circle-outline",class:"cursor-pointer",onClick:Z=>x(o)},null,8,["onClick"]),i("a",{href:o.audio_url,download:"",target:"_blank"},[w(m(q),{icon:"mdi:download",class:"cursor-pointer"})],8,uo)])])],2)}),256))])):(y(),z("div",co,[w(m(ht),{description:r.$t("suno.nodata")},null,8,["description"])]))}}),ho={key:0},fo={class:"w-full relative h-[300px]"},po={class:"w-full h-full justify-center items-center flex"},mo={class:"absolute bottom-0 right-0 p-2 text-white text-right"},bo={class:"text-xl"},go={class:""},yo={class:"text-wrap p-2"},xo={key:1,class:"flex w-full h-full justify-center items-center"},wo=ne({__name:"mcplayer",setup(e){const n=D();return de(()=>A.myData.act,d=>{if(d=="goPlay"){let h=A.myData.actData;n.value=h}}),(d,h)=>n.value?(y(),z("div",ho,[i("div",fo,[w(m(je),{src:n.value.image_large_url,class:"w-full h-full"},{placeholder:T(()=>[i("div",po,[w(m(q),{icon:"line-md:downloading-loop",class:"text-[60px] text-green-300"})])]),_:1},8,["src"]),i("div",mo,[i("h2",bo,g(n.value.title),1),i("div",go,g(d.$t("suno.style"))+"："+g(n.value.metadata.tags),1)])]),i("pre",yo,g(n.value.metadata.prompt),1)])):(y(),z("div",xo,[w(m(ht),{description:d.$t("suno.emputy")},null,8,["description"])]))}}),_o={class:"flex w-full h-full music-content"},ko={class:"w-[300px] h-full overflow-y-auto"},$o={class:"flex-1 h-full bg-[#fafbfc] pt-2 dark:bg-[#18181c] overflow-y-auto music-list"},zo={class:"w-[300px] h-full overflow-y-auto"},Co=ne({__name:"music",setup(e){return(n,d)=>(y(),z("div",_o,[i("div",ko,[w(Aa)]),i("div",$o,[w(vo)]),i("div",zo,[w(wo)])]))}});export{Co as default};
