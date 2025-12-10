import{d as re,w as i,bp as Re,h as se,i as Ie,r as j,n as M,j as de,K as Te,t as oe,F as x,e as R,f as p,H as I,I as q,bI as Ft,bf as zt,bg as St,bq as $e,bt as Mt,k as te,cN as Pt,L as Ne,c6 as B,q as be,cj as Bt,c7 as Rt,bB as It,bl as Tt,cO as je,p as $t,a4 as Nt,C as jt,cn as At,D as Ot,bF as ue,as as he,cP as _t,cQ as Ut,cR as me,cS as Ae,a_ as Dt,cT as pe,G as Vt,cU as Et,cr as Ht,bK as fe,bk as Lt,N as ge,aS as Kt,X as ke,bD as ne,v as qt}from"./index-fc2ca07d.js";import{a as we,B as xe,b as ye,F as Ce}from"./Forward-86f34074.js";function Fe(e){switch(e){case"tiny":return"mini";case"small":return"tiny";case"medium":return"small";case"large":return"medium";case"huge":return"large"}throw new Error(`${e} has no smaller size.`)}const ze=re({name:"More",render(){return i("svg",{viewBox:"0 0 16 16",version:"1.1",xmlns:"http://www.w3.org/2000/svg"},i("g",{stroke:"none","stroke-width":"1",fill:"none","fill-rule":"evenodd"},i("g",{fill:"currentColor","fill-rule":"nonzero"},i("path",{d:"M4,7 C4.55228,7 5,7.44772 5,8 C5,8.55229 4.55228,9 4,9 C3.44772,9 3,8.55229 3,8 C3,7.44772 3.44772,7 4,7 Z M8,7 C8.55229,7 9,7.44772 9,8 C9,8.55229 8.55229,9 8,9 C7.44772,9 7,8.55229 7,8 C7,7.44772 7.44772,7 8,7 Z M12,7 C12.5523,7 13,7.44772 13,8 C13,8.55229 12.5523,9 12,9 C11.4477,9 11,8.55229 11,8 C11,7.44772 11.4477,7 12,7 Z"}))))}}),Oe=Re("n-checkbox-group"),Jt={min:Number,max:Number,size:String,value:Array,defaultValue:{type:Array,default:null},disabled:{type:Boolean,default:void 0},"onUpdate:value":[Function,Array],onUpdateValue:[Function,Array],onChange:[Function,Array]},sa=re({name:"CheckboxGroup",props:Jt,setup(e){const{mergedClsPrefixRef:t}=se(e),o=Ie(e),{mergedSizeRef:s,mergedDisabledRef:w}=o,g=j(e.defaultValue),y=M(()=>e.value),u=de(y,g),h=M(()=>{var d;return((d=u.value)===null||d===void 0?void 0:d.length)||0}),n=M(()=>Array.isArray(u.value)?new Set(u.value):new Set);function k(d,r){const{nTriggerFormInput:b,nTriggerFormChange:v}=o,{onChange:l,"onUpdate:value":m,onUpdateValue:S}=e;if(Array.isArray(u.value)){const C=Array.from(u.value),H=C.findIndex(J=>J===r);d?~H||(C.push(r),S&&x(S,C,{actionType:"check",value:r}),m&&x(m,C,{actionType:"check",value:r}),b(),v(),g.value=C,l&&x(l,C)):~H&&(C.splice(H,1),S&&x(S,C,{actionType:"uncheck",value:r}),m&&x(m,C,{actionType:"uncheck",value:r}),l&&x(l,C),g.value=C,b(),v())}else d?(S&&x(S,[r],{actionType:"check",value:r}),m&&x(m,[r],{actionType:"check",value:r}),l&&x(l,[r]),g.value=[r],b(),v()):(S&&x(S,[],{actionType:"uncheck",value:r}),m&&x(m,[],{actionType:"uncheck",value:r}),l&&x(l,[]),g.value=[],b(),v())}return Te(Oe,{checkedCountRef:h,maxRef:oe(e,"max"),minRef:oe(e,"min"),valueSetRef:n,disabledRef:w,mergedSizeRef:s,toggleCheckbox:k}),{mergedClsPrefix:t}},render(){return i("div",{class:`${this.mergedClsPrefix}-checkbox-group`,role:"group"},this.$slots)}}),Wt=()=>i("svg",{viewBox:"0 0 64 64",class:"check-icon"},i("path",{d:"M50.42,16.76L22.34,39.45l-8.1-11.46c-1.12-1.58-3.3-1.96-4.88-0.84c-1.58,1.12-1.95,3.3-0.84,4.88l10.26,14.51  c0.56,0.79,1.42,1.31,2.38,1.45c0.16,0.02,0.32,0.03,0.48,0.03c0.8,0,1.57-0.27,2.2-0.78l30.99-25.03c1.5-1.21,1.74-3.42,0.52-4.92  C54.13,15.78,51.93,15.55,50.42,16.76z"})),Qt=()=>i("svg",{viewBox:"0 0 100 100",class:"line-icon"},i("path",{d:"M80.2,55.5H21.4c-2.8,0-5.1-2.5-5.1-5.5l0,0c0-3,2.3-5.5,5.1-5.5h58.7c2.8,0,5.1,2.5,5.1,5.5l0,0C85.2,53.1,82.9,55.5,80.2,55.5z"})),Gt=R([p("checkbox",`
 font-size: var(--n-font-size);
 outline: none;
 cursor: pointer;
 display: inline-flex;
 flex-wrap: nowrap;
 align-items: flex-start;
 word-break: break-word;
 line-height: var(--n-size);
 --n-merged-color-table: var(--n-color-table);
 `,[I("show-label","line-height: var(--n-label-line-height);"),R("&:hover",[p("checkbox-box",[q("border","border: var(--n-border-checked);")])]),R("&:focus:not(:active)",[p("checkbox-box",[q("border",`
 border: var(--n-border-focus);
 box-shadow: var(--n-box-shadow-focus);
 `)])]),I("inside-table",[p("checkbox-box",`
 background-color: var(--n-merged-color-table);
 `)]),I("checked",[p("checkbox-box",`
 background-color: var(--n-color-checked);
 `,[p("checkbox-icon",[R(".check-icon",`
 opacity: 1;
 transform: scale(1);
 `)])])]),I("indeterminate",[p("checkbox-box",[p("checkbox-icon",[R(".check-icon",`
 opacity: 0;
 transform: scale(.5);
 `),R(".line-icon",`
 opacity: 1;
 transform: scale(1);
 `)])])]),I("checked, indeterminate",[R("&:focus:not(:active)",[p("checkbox-box",[q("border",`
 border: var(--n-border-checked);
 box-shadow: var(--n-box-shadow-focus);
 `)])]),p("checkbox-box",`
 background-color: var(--n-color-checked);
 border-left: 0;
 border-top: 0;
 `,[q("border",{border:"var(--n-border-checked)"})])]),I("disabled",{cursor:"not-allowed"},[I("checked",[p("checkbox-box",`
 background-color: var(--n-color-disabled-checked);
 `,[q("border",{border:"var(--n-border-disabled-checked)"}),p("checkbox-icon",[R(".check-icon, .line-icon",{fill:"var(--n-check-mark-color-disabled-checked)"})])])]),p("checkbox-box",`
 background-color: var(--n-color-disabled);
 `,[q("border",`
 border: var(--n-border-disabled);
 `),p("checkbox-icon",[R(".check-icon, .line-icon",`
 fill: var(--n-check-mark-color-disabled);
 `)])]),q("label",`
 color: var(--n-text-color-disabled);
 `)]),p("checkbox-box-wrapper",`
 position: relative;
 width: var(--n-size);
 flex-shrink: 0;
 flex-grow: 0;
 user-select: none;
 -webkit-user-select: none;
 `),p("checkbox-box",`
 position: absolute;
 left: 0;
 top: 50%;
 transform: translateY(-50%);
 height: var(--n-size);
 width: var(--n-size);
 display: inline-block;
 box-sizing: border-box;
 border-radius: var(--n-border-radius);
 background-color: var(--n-color);
 transition: background-color 0.3s var(--n-bezier);
 `,[q("border",`
 transition:
 border-color .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier);
 border-radius: inherit;
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 border: var(--n-border);
 `),p("checkbox-icon",`
 display: flex;
 align-items: center;
 justify-content: center;
 position: absolute;
 left: 1px;
 right: 1px;
 top: 1px;
 bottom: 1px;
 `,[R(".check-icon, .line-icon",`
 width: 100%;
 fill: var(--n-check-mark-color);
 opacity: 0;
 transform: scale(0.5);
 transform-origin: center;
 transition:
 fill 0.3s var(--n-bezier),
 transform 0.3s var(--n-bezier),
 opacity 0.3s var(--n-bezier),
 border-color 0.3s var(--n-bezier);
 `),Ft({left:"1px",top:"1px"})])]),q("label",`
 color: var(--n-text-color);
 transition: color .3s var(--n-bezier);
 user-select: none;
 -webkit-user-select: none;
 padding: var(--n-label-padding);
 font-weight: var(--n-label-font-weight);
 `,[R("&:empty",{display:"none"})])]),zt(p("checkbox",`
 --n-merged-color-table: var(--n-color-table-modal);
 `)),St(p("checkbox",`
 --n-merged-color-table: var(--n-color-table-popover);
 `))]),Zt=Object.assign(Object.assign({},te.props),{size:String,checked:{type:[Boolean,String,Number],default:void 0},defaultChecked:{type:[Boolean,String,Number],default:!1},value:[String,Number],disabled:{type:Boolean,default:void 0},indeterminate:Boolean,label:String,focusable:{type:Boolean,default:!0},checkedValue:{type:[Boolean,String,Number],default:!0},uncheckedValue:{type:[Boolean,String,Number],default:!1},"onUpdate:checked":[Function,Array],onUpdateChecked:[Function,Array],privateInsideTable:Boolean,onChange:[Function,Array]}),da=re({name:"Checkbox",props:Zt,setup(e){const t=$e(Oe,null),o=j(null),{mergedClsPrefixRef:s,inlineThemeDisabled:w,mergedRtlRef:g}=se(e),y=j(e.defaultChecked),u=oe(e,"checked"),h=de(u,y),n=Mt(()=>{if(t){const c=t.valueSetRef.value;return c&&e.value!==void 0?c.has(e.value):!1}else return h.value===e.checkedValue}),k=Ie(e,{mergedSize(c){const{size:F}=e;if(F!==void 0)return F;if(t){const{value:P}=t.mergedSizeRef;if(P!==void 0)return P}if(c){const{mergedSize:P}=c;if(P!==void 0)return P.value}return"medium"},mergedDisabled(c){const{disabled:F}=e;if(F!==void 0)return F;if(t){if(t.disabledRef.value)return!0;const{maxRef:{value:P},checkedCountRef:A}=t;if(P!==void 0&&A.value>=P&&!n.value)return!0;const{minRef:{value:D}}=t;if(D!==void 0&&A.value<=D&&n.value)return!0}return c?c.disabled.value:!1}}),{mergedDisabledRef:d,mergedSizeRef:r}=k,b=te("Checkbox","-checkbox",Gt,Pt,e,s);function v(c){if(t&&e.value!==void 0)t.toggleCheckbox(!n.value,e.value);else{const{onChange:F,"onUpdate:checked":P,onUpdateChecked:A}=e,{nTriggerFormInput:D,nTriggerFormChange:W}=k,O=n.value?e.uncheckedValue:e.checkedValue;P&&x(P,O,c),A&&x(A,O,c),F&&x(F,O,c),D(),W(),y.value=O}}function l(c){d.value||v(c)}function m(c){if(!d.value)switch(c.key){case" ":case"Enter":v(c)}}function S(c){switch(c.key){case" ":c.preventDefault()}}const C={focus:()=>{var c;(c=o.value)===null||c===void 0||c.focus()},blur:()=>{var c;(c=o.value)===null||c===void 0||c.blur()}},H=Ne("Checkbox",g,s),J=M(()=>{const{value:c}=r,{common:{cubicBezierEaseInOut:F},self:{borderRadius:P,color:A,colorChecked:D,colorDisabled:W,colorTableHeader:O,colorTableHeaderModal:Q,colorTableHeaderPopover:ae,checkMarkColor:V,checkMarkColorDisabled:$,border:G,borderFocus:E,borderDisabled:ie,borderChecked:z,boxShadowFocus:le,textColor:_,textColorDisabled:Z,checkMarkColorDisabledChecked:X,colorDisabledChecked:N,borderDisabledChecked:Y,labelPadding:L,labelLineHeight:T,labelFontWeight:a,[B("fontSize",c)]:f,[B("size",c)]:K}}=b.value;return{"--n-label-line-height":T,"--n-label-font-weight":a,"--n-size":K,"--n-bezier":F,"--n-border-radius":P,"--n-border":G,"--n-border-checked":z,"--n-border-focus":E,"--n-border-disabled":ie,"--n-border-disabled-checked":Y,"--n-box-shadow-focus":le,"--n-color":A,"--n-color-checked":D,"--n-color-table":O,"--n-color-table-modal":Q,"--n-color-table-popover":ae,"--n-color-disabled":W,"--n-color-disabled-checked":N,"--n-text-color":_,"--n-text-color-disabled":Z,"--n-check-mark-color":V,"--n-check-mark-color-disabled":$,"--n-check-mark-color-disabled-checked":X,"--n-font-size":f,"--n-label-padding":L}}),U=w?be("checkbox",M(()=>r.value[0]),J,e):void 0;return Object.assign(k,C,{rtlEnabled:H,selfRef:o,mergedClsPrefix:s,mergedDisabled:d,renderedChecked:n,mergedTheme:b,labelId:Bt(),handleClick:l,handleKeyUp:m,handleKeyDown:S,cssVars:w?void 0:J,themeClass:U==null?void 0:U.themeClass,onRender:U==null?void 0:U.onRender})},render(){var e;const{$slots:t,renderedChecked:o,mergedDisabled:s,indeterminate:w,privateInsideTable:g,cssVars:y,labelId:u,label:h,mergedClsPrefix:n,focusable:k,handleKeyUp:d,handleKeyDown:r,handleClick:b}=this;(e=this.onRender)===null||e===void 0||e.call(this);const v=Rt(t.default,l=>h||l?i("span",{class:`${n}-checkbox__label`,id:u},h||l):null);return i("div",{ref:"selfRef",class:[`${n}-checkbox`,this.themeClass,this.rtlEnabled&&`${n}-checkbox--rtl`,o&&`${n}-checkbox--checked`,s&&`${n}-checkbox--disabled`,w&&`${n}-checkbox--indeterminate`,g&&`${n}-checkbox--inside-table`,v&&`${n}-checkbox--show-label`],tabindex:s||!k?void 0:0,role:"checkbox","aria-checked":w?"mixed":o,"aria-labelledby":u,style:y,onKeyup:d,onKeydown:r,onClick:b,onMousedown:()=>{Tt("selectstart",window,l=>{l.preventDefault()},{once:!0})}},i("div",{class:`${n}-checkbox-box-wrapper`}," ",i("div",{class:`${n}-checkbox-box`},i(It,null,{default:()=>this.indeterminate?i("div",{key:"indeterminate",class:`${n}-checkbox-icon`},Qt()):i("div",{key:"check",class:`${n}-checkbox-icon`},Wt())}),i("div",{class:`${n}-checkbox-box__border`}))),v)}}),_e=Re("n-popselect"),Xt=p("popselect-menu",`
 box-shadow: var(--n-menu-box-shadow);
`),ve={multiple:Boolean,value:{type:[String,Number,Array],default:null},cancelable:Boolean,options:{type:Array,default:()=>[]},size:{type:String,default:"medium"},scrollable:Boolean,"onUpdate:value":[Function,Array],onUpdateValue:[Function,Array],onMouseenter:Function,onMouseleave:Function,renderLabel:Function,showCheckmark:{type:Boolean,default:void 0},nodeProps:Function,virtualScroll:Boolean,onChange:[Function,Array]},Se=At(ve),Yt=re({name:"PopselectPanel",props:ve,setup(e){const t=$e(_e),{mergedClsPrefixRef:o,inlineThemeDisabled:s}=se(e),w=te("Popselect","-pop-select",Xt,je,t.props,o),g=M(()=>$t(e.options,Ot("value","children")));function y(r,b){const{onUpdateValue:v,"onUpdate:value":l,onChange:m}=e;v&&x(v,r,b),l&&x(l,r,b),m&&x(m,r,b)}function u(r){n(r.key)}function h(r){!ue(r,"action")&&!ue(r,"empty")&&!ue(r,"header")&&r.preventDefault()}function n(r){const{value:{getNode:b}}=g;if(e.multiple)if(Array.isArray(e.value)){const v=[],l=[];let m=!0;e.value.forEach(S=>{if(S===r){m=!1;return}const C=b(S);C&&(v.push(C.key),l.push(C.rawNode))}),m&&(v.push(r),l.push(b(r).rawNode)),y(v,l)}else{const v=b(r);v&&y([r],[v.rawNode])}else if(e.value===r&&e.cancelable)y(null,null);else{const v=b(r);v&&y(r,v.rawNode);const{"onUpdate:show":l,onUpdateShow:m}=t.props;l&&x(l,!1),m&&x(m,!1),t.setShow(!1)}he(()=>{t.syncPosition()})}Nt(oe(e,"options"),()=>{he(()=>{t.syncPosition()})});const k=M(()=>{const{self:{menuBoxShadow:r}}=w.value;return{"--n-menu-box-shadow":r}}),d=s?be("select",void 0,k,t.props):void 0;return{mergedTheme:t.mergedThemeRef,mergedClsPrefix:o,treeMate:g,handleToggle:u,handleMenuMousedown:h,cssVars:s?void 0:k,themeClass:d==null?void 0:d.themeClass,onRender:d==null?void 0:d.onRender}},render(){var e;return(e=this.onRender)===null||e===void 0||e.call(this),i(jt,{clsPrefix:this.mergedClsPrefix,focusable:!0,nodeProps:this.nodeProps,class:[`${this.mergedClsPrefix}-popselect-menu`,this.themeClass],style:this.cssVars,theme:this.mergedTheme.peers.InternalSelectMenu,themeOverrides:this.mergedTheme.peerOverrides.InternalSelectMenu,multiple:this.multiple,treeMate:this.treeMate,size:this.size,value:this.value,virtualScroll:this.virtualScroll,scrollable:this.scrollable,renderLabel:this.renderLabel,onToggle:this.handleToggle,onMouseenter:this.onMouseenter,onMouseleave:this.onMouseenter,onMousedown:this.handleMenuMousedown,showCheckmark:this.showCheckmark},{header:()=>{var t,o;return((o=(t=this.$slots).header)===null||o===void 0?void 0:o.call(t))||[]},action:()=>{var t,o;return((o=(t=this.$slots).action)===null||o===void 0?void 0:o.call(t))||[]},empty:()=>{var t,o;return((o=(t=this.$slots).empty)===null||o===void 0?void 0:o.call(t))||[]}})}}),ea=Object.assign(Object.assign(Object.assign(Object.assign({},te.props),Ae(pe,["showArrow","arrow"])),{placement:Object.assign(Object.assign({},pe.placement),{default:"bottom"}),trigger:{type:String,default:"hover"}}),ve),ta=re({name:"Popselect",props:ea,slots:Object,inheritAttrs:!1,__popover__:!0,setup(e){const{mergedClsPrefixRef:t}=se(e),o=te("Popselect","-popselect",void 0,je,e,t),s=j(null);function w(){var u;(u=s.value)===null||u===void 0||u.syncPosition()}function g(u){var h;(h=s.value)===null||h===void 0||h.setShow(u)}return Te(_e,{props:e,mergedThemeRef:o,syncPosition:w,setShow:g}),Object.assign(Object.assign({},{syncPosition:w,setShow:g}),{popoverInstRef:s,mergedTheme:o})},render(){const{mergedTheme:e}=this,t={theme:e.peers.Popover,themeOverrides:e.peerOverrides.Popover,builtinThemeOverrides:{padding:"0"},ref:"popoverInstRef",internalRenderBody:(o,s,w,g,y)=>{const{$attrs:u}=this;return i(Yt,Object.assign({},u,{class:[u.class,o],style:[u.style,...w]},_t(this.$props,Se),{ref:Ut(s),onMouseenter:me([g,u.onMouseenter]),onMouseleave:me([y,u.onMouseleave])}),{header:()=>{var h,n;return(n=(h=this.$slots).header)===null||n===void 0?void 0:n.call(h)},action:()=>{var h,n;return(n=(h=this.$slots).action)===null||n===void 0?void 0:n.call(h)},empty:()=>{var h,n;return(n=(h=this.$slots).empty)===null||n===void 0?void 0:n.call(h)}})}};return i(Dt,Object.assign({},Ae(this.$props,Se),t,{internalDeactivateImmediately:!0}),{trigger:()=>{var o,s;return(s=(o=this.$slots).default)===null||s===void 0?void 0:s.call(o)}})}}),Me=`
 background: var(--n-item-color-hover);
 color: var(--n-item-text-color-hover);
 border: var(--n-item-border-hover);
`,Pe=[I("button",`
 background: var(--n-button-color-hover);
 border: var(--n-button-border-hover);
 color: var(--n-button-icon-color-hover);
 `)],aa=p("pagination",`
 display: flex;
 vertical-align: middle;
 font-size: var(--n-item-font-size);
 flex-wrap: nowrap;
`,[p("pagination-prefix",`
 display: flex;
 align-items: center;
 margin: var(--n-prefix-margin);
 `),p("pagination-suffix",`
 display: flex;
 align-items: center;
 margin: var(--n-suffix-margin);
 `),R("> *:not(:first-child)",`
 margin: var(--n-item-margin);
 `),p("select",`
 width: var(--n-select-width);
 `),R("&.transition-disabled",[p("pagination-item","transition: none!important;")]),p("pagination-quick-jumper",`
 white-space: nowrap;
 display: flex;
 color: var(--n-jumper-text-color);
 transition: color .3s var(--n-bezier);
 align-items: center;
 font-size: var(--n-jumper-font-size);
 `,[p("input",`
 margin: var(--n-input-margin);
 width: var(--n-input-width);
 `)]),p("pagination-item",`
 position: relative;
 cursor: pointer;
 user-select: none;
 -webkit-user-select: none;
 display: flex;
 align-items: center;
 justify-content: center;
 box-sizing: border-box;
 min-width: var(--n-item-size);
 height: var(--n-item-size);
 padding: var(--n-item-padding);
 background-color: var(--n-item-color);
 color: var(--n-item-text-color);
 border-radius: var(--n-item-border-radius);
 border: var(--n-item-border);
 fill: var(--n-button-icon-color);
 transition:
 color .3s var(--n-bezier),
 border-color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 fill .3s var(--n-bezier);
 `,[I("button",`
 background: var(--n-button-color);
 color: var(--n-button-icon-color);
 border: var(--n-button-border);
 padding: 0;
 `,[p("base-icon",`
 font-size: var(--n-button-icon-size);
 `)]),Vt("disabled",[I("hover",Me,Pe),R("&:hover",Me,Pe),R("&:active",`
 background: var(--n-item-color-pressed);
 color: var(--n-item-text-color-pressed);
 border: var(--n-item-border-pressed);
 `,[I("button",`
 background: var(--n-button-color-pressed);
 border: var(--n-button-border-pressed);
 color: var(--n-button-icon-color-pressed);
 `)]),I("active",`
 background: var(--n-item-color-active);
 color: var(--n-item-text-color-active);
 border: var(--n-item-border-active);
 `,[R("&:hover",`
 background: var(--n-item-color-active-hover);
 `)])]),I("disabled",`
 cursor: not-allowed;
 color: var(--n-item-text-color-disabled);
 `,[I("active, button",`
 background-color: var(--n-item-color-disabled);
 border: var(--n-item-border-disabled);
 `)])]),I("disabled",`
 cursor: not-allowed;
 `,[p("pagination-quick-jumper",`
 color: var(--n-jumper-text-color-disabled);
 `)]),I("simple",`
 display: flex;
 align-items: center;
 flex-wrap: nowrap;
 `,[p("pagination-quick-jumper",[p("input",`
 margin: 0;
 `)])])]);function na(e){var t;if(!e)return 10;const{defaultPageSize:o}=e;if(o!==void 0)return o;const s=(t=e.pageSizes)===null||t===void 0?void 0:t[0];return typeof s=="number"?s:(s==null?void 0:s.value)||10}function oa(e,t,o,s){let w=!1,g=!1,y=1,u=t;if(t===1)return{hasFastBackward:!1,hasFastForward:!1,fastForwardTo:u,fastBackwardTo:y,items:[{type:"page",label:1,active:e===1,mayBeFastBackward:!1,mayBeFastForward:!1}]};if(t===2)return{hasFastBackward:!1,hasFastForward:!1,fastForwardTo:u,fastBackwardTo:y,items:[{type:"page",label:1,active:e===1,mayBeFastBackward:!1,mayBeFastForward:!1},{type:"page",label:2,active:e===2,mayBeFastBackward:!0,mayBeFastForward:!1}]};const h=1,n=t;let k=e,d=e;const r=(o-5)/2;d+=Math.ceil(r),d=Math.min(Math.max(d,h+o-3),n-2),k-=Math.floor(r),k=Math.max(Math.min(k,n-o+3),h+2);let b=!1,v=!1;k>h+2&&(b=!0),d<n-2&&(v=!0);const l=[];l.push({type:"page",label:1,active:e===1,mayBeFastBackward:!1,mayBeFastForward:!1}),b?(w=!0,y=k-1,l.push({type:"fast-backward",active:!1,label:void 0,options:s?Be(h+1,k-1):null})):n>=h+1&&l.push({type:"page",label:h+1,mayBeFastBackward:!0,mayBeFastForward:!1,active:e===h+1});for(let m=k;m<=d;++m)l.push({type:"page",label:m,mayBeFastBackward:!1,mayBeFastForward:!1,active:e===m});return v?(g=!0,u=d+1,l.push({type:"fast-forward",active:!1,label:void 0,options:s?Be(d+1,n-1):null})):d===n-2&&l[l.length-1].label!==n-1&&l.push({type:"page",mayBeFastForward:!0,mayBeFastBackward:!1,label:n-1,active:e===n-1}),l[l.length-1].label!==n&&l.push({type:"page",mayBeFastForward:!1,mayBeFastBackward:!1,label:n,active:e===n}),{hasFastBackward:w,hasFastForward:g,fastBackwardTo:y,fastForwardTo:u,items:l}}function Be(e,t){const o=[];for(let s=e;s<=t;++s)o.push({label:`${s}`,value:s});return o}const ra=Object.assign(Object.assign({},te.props),{simple:Boolean,page:Number,defaultPage:{type:Number,default:1},itemCount:Number,pageCount:Number,defaultPageCount:{type:Number,default:1},showSizePicker:Boolean,pageSize:Number,defaultPageSize:Number,pageSizes:{type:Array,default(){return[10]}},showQuickJumper:Boolean,size:{type:String,default:"medium"},disabled:Boolean,pageSlot:{type:Number,default:9},selectProps:Object,prev:Function,next:Function,goto:Function,prefix:Function,suffix:Function,label:Function,displayOrder:{type:Array,default:["pages","size-picker","quick-jumper"]},to:qt.propTo,showQuickJumpDropdown:{type:Boolean,default:!0},"onUpdate:page":[Function,Array],onUpdatePage:[Function,Array],"onUpdate:pageSize":[Function,Array],onUpdatePageSize:[Function,Array],onPageSizeChange:[Function,Array],onChange:[Function,Array]}),ca=re({name:"Pagination",props:ra,slots:Object,setup(e){const{mergedComponentPropsRef:t,mergedClsPrefixRef:o,inlineThemeDisabled:s,mergedRtlRef:w}=se(e),g=te("Pagination","-pagination",aa,Et,e,o),{localeRef:y}=Ht("Pagination"),u=j(null),h=j(e.defaultPage),n=j(na(e)),k=de(oe(e,"page"),h),d=de(oe(e,"pageSize"),n),r=M(()=>{const{itemCount:a}=e;if(a!==void 0)return Math.max(1,Math.ceil(a/d.value));const{pageCount:f}=e;return f!==void 0?Math.max(f,1):1}),b=j("");fe(()=>{e.simple,b.value=String(k.value)});const v=j(!1),l=j(!1),m=j(!1),S=j(!1),C=()=>{e.disabled||(v.value=!0,V())},H=()=>{e.disabled||(v.value=!1,V())},J=()=>{l.value=!0,V()},U=()=>{l.value=!1,V()},c=a=>{$(a)},F=M(()=>oa(k.value,r.value,e.pageSlot,e.showQuickJumpDropdown));fe(()=>{F.value.hasFastBackward?F.value.hasFastForward||(v.value=!1,m.value=!1):(l.value=!1,S.value=!1)});const P=M(()=>{const a=y.value.selectionSuffix;return e.pageSizes.map(f=>typeof f=="number"?{label:`${f} / ${a}`,value:f}:f)}),A=M(()=>{var a,f;return((f=(a=t==null?void 0:t.value)===null||a===void 0?void 0:a.Pagination)===null||f===void 0?void 0:f.inputSize)||Fe(e.size)}),D=M(()=>{var a,f;return((f=(a=t==null?void 0:t.value)===null||a===void 0?void 0:a.Pagination)===null||f===void 0?void 0:f.selectSize)||Fe(e.size)}),W=M(()=>(k.value-1)*d.value),O=M(()=>{const a=k.value*d.value-1,{itemCount:f}=e;return f!==void 0&&a>f-1?f-1:a}),Q=M(()=>{const{itemCount:a}=e;return a!==void 0?a:(e.pageCount||1)*d.value}),ae=Ne("Pagination",w,o);function V(){he(()=>{var a;const{value:f}=u;f&&(f.classList.add("transition-disabled"),(a=u.value)===null||a===void 0||a.offsetWidth,f.classList.remove("transition-disabled"))})}function $(a){if(a===k.value)return;const{"onUpdate:page":f,onUpdatePage:K,onChange:ee,simple:ce}=e;f&&x(f,a),K&&x(K,a),ee&&x(ee,a),h.value=a,ce&&(b.value=String(a))}function G(a){if(a===d.value)return;const{"onUpdate:pageSize":f,onUpdatePageSize:K,onPageSizeChange:ee}=e;f&&x(f,a),K&&x(K,a),ee&&x(ee,a),n.value=a,r.value<k.value&&$(r.value)}function E(){if(e.disabled)return;const a=Math.min(k.value+1,r.value);$(a)}function ie(){if(e.disabled)return;const a=Math.max(k.value-1,1);$(a)}function z(){if(e.disabled)return;const a=Math.min(F.value.fastForwardTo,r.value);$(a)}function le(){if(e.disabled)return;const a=Math.max(F.value.fastBackwardTo,1);$(a)}function _(a){G(a)}function Z(){const a=Number.parseInt(b.value);Number.isNaN(a)||($(Math.max(1,Math.min(a,r.value))),e.simple||(b.value=""))}function X(){Z()}function N(a){if(!e.disabled)switch(a.type){case"page":$(a.label);break;case"fast-backward":le();break;case"fast-forward":z();break}}function Y(a){b.value=a.replace(/\D+/g,"")}fe(()=>{k.value,d.value,V()});const L=M(()=>{const{size:a}=e,{self:{buttonBorder:f,buttonBorderHover:K,buttonBorderPressed:ee,buttonIconColor:ce,buttonIconColorHover:Ue,buttonIconColorPressed:De,itemTextColor:Ve,itemTextColorHover:Ee,itemTextColorPressed:He,itemTextColorActive:Le,itemTextColorDisabled:Ke,itemColor:qe,itemColorHover:Je,itemColorPressed:We,itemColorActive:Qe,itemColorActiveHover:Ge,itemColorDisabled:Ze,itemBorder:Xe,itemBorderHover:Ye,itemBorderPressed:et,itemBorderActive:tt,itemBorderDisabled:at,itemBorderRadius:nt,jumperTextColor:ot,jumperTextColorDisabled:rt,buttonColor:it,buttonColorHover:lt,buttonColorPressed:st,[B("itemPadding",a)]:dt,[B("itemMargin",a)]:ct,[B("inputWidth",a)]:ut,[B("selectWidth",a)]:ft,[B("inputMargin",a)]:ht,[B("selectMargin",a)]:bt,[B("jumperFontSize",a)]:vt,[B("prefixMargin",a)]:mt,[B("suffixMargin",a)]:pt,[B("itemSize",a)]:gt,[B("buttonIconSize",a)]:kt,[B("itemFontSize",a)]:wt,[`${B("itemMargin",a)}Rtl`]:xt,[`${B("inputMargin",a)}Rtl`]:yt},common:{cubicBezierEaseInOut:Ct}}=g.value;return{"--n-prefix-margin":mt,"--n-suffix-margin":pt,"--n-item-font-size":wt,"--n-select-width":ft,"--n-select-margin":bt,"--n-input-width":ut,"--n-input-margin":ht,"--n-input-margin-rtl":yt,"--n-item-size":gt,"--n-item-text-color":Ve,"--n-item-text-color-disabled":Ke,"--n-item-text-color-hover":Ee,"--n-item-text-color-active":Le,"--n-item-text-color-pressed":He,"--n-item-color":qe,"--n-item-color-hover":Je,"--n-item-color-disabled":Ze,"--n-item-color-active":Qe,"--n-item-color-active-hover":Ge,"--n-item-color-pressed":We,"--n-item-border":Xe,"--n-item-border-hover":Ye,"--n-item-border-disabled":at,"--n-item-border-active":tt,"--n-item-border-pressed":et,"--n-item-padding":dt,"--n-item-border-radius":nt,"--n-bezier":Ct,"--n-jumper-font-size":vt,"--n-jumper-text-color":ot,"--n-jumper-text-color-disabled":rt,"--n-item-margin":ct,"--n-item-margin-rtl":xt,"--n-button-icon-size":kt,"--n-button-icon-color":ce,"--n-button-icon-color-hover":Ue,"--n-button-icon-color-pressed":De,"--n-button-color-hover":lt,"--n-button-color":it,"--n-button-color-pressed":st,"--n-button-border":f,"--n-button-border-hover":K,"--n-button-border-pressed":ee}}),T=s?be("pagination",M(()=>{let a="";const{size:f}=e;return a+=f[0],a}),L,e):void 0;return{rtlEnabled:ae,mergedClsPrefix:o,locale:y,selfRef:u,mergedPage:k,pageItems:M(()=>F.value.items),mergedItemCount:Q,jumperValue:b,pageSizeOptions:P,mergedPageSize:d,inputSize:A,selectSize:D,mergedTheme:g,mergedPageCount:r,startIndex:W,endIndex:O,showFastForwardMenu:m,showFastBackwardMenu:S,fastForwardActive:v,fastBackwardActive:l,handleMenuSelect:c,handleFastForwardMouseenter:C,handleFastForwardMouseleave:H,handleFastBackwardMouseenter:J,handleFastBackwardMouseleave:U,handleJumperInput:Y,handleBackwardClick:ie,handleForwardClick:E,handlePageItemClick:N,handleSizePickerChange:_,handleQuickJumperChange:X,cssVars:s?void 0:L,themeClass:T==null?void 0:T.themeClass,onRender:T==null?void 0:T.onRender}},render(){const{$slots:e,mergedClsPrefix:t,disabled:o,cssVars:s,mergedPage:w,mergedPageCount:g,pageItems:y,showSizePicker:u,showQuickJumper:h,mergedTheme:n,locale:k,inputSize:d,selectSize:r,mergedPageSize:b,pageSizeOptions:v,jumperValue:l,simple:m,prev:S,next:C,prefix:H,suffix:J,label:U,goto:c,handleJumperInput:F,handleSizePickerChange:P,handleBackwardClick:A,handlePageItemClick:D,handleForwardClick:W,handleQuickJumperChange:O,onRender:Q}=this;Q==null||Q();const ae=H||e.prefix,V=J||e.suffix,$=S||e.prev,G=C||e.next,E=U||e.label;return i("div",{ref:"selfRef",class:[`${t}-pagination`,this.themeClass,this.rtlEnabled&&`${t}-pagination--rtl`,o&&`${t}-pagination--disabled`,m&&`${t}-pagination--simple`],style:s},ae?i("div",{class:`${t}-pagination-prefix`},ae({page:w,pageSize:b,pageCount:g,startIndex:this.startIndex,endIndex:this.endIndex,itemCount:this.mergedItemCount})):null,this.displayOrder.map(ie=>{switch(ie){case"pages":return i(ke,null,i("div",{class:[`${t}-pagination-item`,!$&&`${t}-pagination-item--button`,(w<=1||w>g||o)&&`${t}-pagination-item--disabled`],onClick:A},$?$({page:w,pageSize:b,pageCount:g,startIndex:this.startIndex,endIndex:this.endIndex,itemCount:this.mergedItemCount}):i(ne,{clsPrefix:t},{default:()=>this.rtlEnabled?i(we,null):i(xe,null)})),m?i(ke,null,i("div",{class:`${t}-pagination-quick-jumper`},i(ge,{value:l,onUpdateValue:F,size:d,placeholder:"",disabled:o,theme:n.peers.Input,themeOverrides:n.peerOverrides.Input,onChange:O}))," /"," ",g):y.map((z,le)=>{let _,Z,X;const{type:N}=z;switch(N){case"page":const L=z.label;E?_=E({type:"page",node:L,active:z.active}):_=L;break;case"fast-forward":const T=this.fastForwardActive?i(ne,{clsPrefix:t},{default:()=>this.rtlEnabled?i(Ce,null):i(ye,null)}):i(ne,{clsPrefix:t},{default:()=>i(ze,null)});E?_=E({type:"fast-forward",node:T,active:this.fastForwardActive||this.showFastForwardMenu}):_=T,Z=this.handleFastForwardMouseenter,X=this.handleFastForwardMouseleave;break;case"fast-backward":const a=this.fastBackwardActive?i(ne,{clsPrefix:t},{default:()=>this.rtlEnabled?i(ye,null):i(Ce,null)}):i(ne,{clsPrefix:t},{default:()=>i(ze,null)});E?_=E({type:"fast-backward",node:a,active:this.fastBackwardActive||this.showFastBackwardMenu}):_=a,Z=this.handleFastBackwardMouseenter,X=this.handleFastBackwardMouseleave;break}const Y=i("div",{key:le,class:[`${t}-pagination-item`,z.active&&`${t}-pagination-item--active`,N!=="page"&&(N==="fast-backward"&&this.showFastBackwardMenu||N==="fast-forward"&&this.showFastForwardMenu)&&`${t}-pagination-item--hover`,o&&`${t}-pagination-item--disabled`,N==="page"&&`${t}-pagination-item--clickable`],onClick:()=>{D(z)},onMouseenter:Z,onMouseleave:X},_);if(N==="page"&&!z.mayBeFastBackward&&!z.mayBeFastForward)return Y;{const L=z.type==="page"?z.mayBeFastBackward?"fast-backward":"fast-forward":z.type;return z.type!=="page"&&!z.options?Y:i(ta,{to:this.to,key:L,disabled:o,trigger:"hover",virtualScroll:!0,style:{width:"60px"},theme:n.peers.Popselect,themeOverrides:n.peerOverrides.Popselect,builtinThemeOverrides:{peers:{InternalSelectMenu:{height:"calc(var(--n-option-height) * 4.6)"}}},nodeProps:()=>({style:{justifyContent:"center"}}),show:N==="page"?!1:N==="fast-backward"?this.showFastBackwardMenu:this.showFastForwardMenu,onUpdateShow:T=>{N!=="page"&&(T?N==="fast-backward"?this.showFastBackwardMenu=T:this.showFastForwardMenu=T:(this.showFastBackwardMenu=!1,this.showFastForwardMenu=!1))},options:z.type!=="page"&&z.options?z.options:[],onUpdateValue:this.handleMenuSelect,scrollable:!0,showCheckmark:!1},{default:()=>Y})}}),i("div",{class:[`${t}-pagination-item`,!G&&`${t}-pagination-item--button`,{[`${t}-pagination-item--disabled`]:w<1||w>=g||o}],onClick:W},G?G({page:w,pageSize:b,pageCount:g,itemCount:this.mergedItemCount,startIndex:this.startIndex,endIndex:this.endIndex}):i(ne,{clsPrefix:t},{default:()=>this.rtlEnabled?i(xe,null):i(we,null)})));case"size-picker":return!m&&u?i(Kt,Object.assign({consistentMenuWidth:!1,placeholder:"",showCheckmark:!1,to:this.to},this.selectProps,{size:r,options:v,value:b,disabled:o,theme:n.peers.Select,themeOverrides:n.peerOverrides.Select,onUpdateValue:P})):null;case"quick-jumper":return!m&&h?i("div",{class:`${t}-pagination-quick-jumper`},c?c():Lt(this.$slots.goto,()=>[k.goto]),i(ge,{value:l,onUpdateValue:F,size:d,placeholder:"",disabled:o,theme:n.peers.Input,themeOverrides:n.peerOverrides.Input,onChange:O})):null;default:return null}}),V?i("div",{class:`${t}-pagination-suffix`},V({page:w,pageSize:b,pageCount:g,startIndex:this.startIndex,endIndex:this.endIndex,itemCount:this.mergedItemCount})):null)}});export{ca as N,da as a,sa as b,na as g};
