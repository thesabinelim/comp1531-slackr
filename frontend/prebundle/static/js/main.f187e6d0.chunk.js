(window.webpackJsonpfrontend=window.webpackJsonpfrontend||[]).push([[0],{151:function(e,a,t){e.exports=t(184)},157:function(e,a,t){},158:function(e,a,t){},184:function(e,a,t){"use strict";t.r(a);var n=t(0),r=t.n(n),l=t(11),o=t.n(l),c=t(246),i=t(245),m=t(14),u=(t(156),t(157),t(9)),s=t(32),d=t(50),f=(t(158),t(48)),p=t(224),E=t(225),g=t(226),h=t(45),b=t(218),v=t(101),y=t(21),k=t(223),_=t(103),O=t.n(_),w=t(8),C=t.n(w),j=r.a.createContext(),S=j.Provider,x=(j.Consumer,j),P="http://localhost:5000",I=t(216),D=t(99),W=t.n(D),F=t(220),N=t(187),R=t(77),L=t(219),T=t(222),z=t(221),V=t(97),A=!1,q=function(){return A},B=function(e){return A=!!e},M=1e3,U=[],J=function(e){return U.push(e)},H=function(e){return Object(V.a)("stepSubscribers"),U=U.filter((function(a){return a!==e}))},K=function(){return U.forEach((function(e){return e()}))},G=["Live","Step"];var $=function(){var e=r.a.useState(!1),a=Object(u.a)(e,2),t=a[0],n=a[1],l=r.a.useRef(null),o=r.a.useState(q()?0:1),c=Object(u.a)(o,2),i=c[0],m=c[1],s=function(e){l.current&&l.current.contains(e.target)||n(!1)};return r.a.createElement(r.a.Fragment,null,r.a.createElement(I.a,{variant:"contained",color:"primary",ref:l,"aria-label":"split button"},r.a.createElement(b.a,{onClick:function(){K()},disabled:0===i},G[i]),r.a.createElement(b.a,{color:"primary",size:"small","aria-owns":t?"menu-list-grow":void 0,"aria-haspopup":"true",onClick:function(){n((function(e){return!e}))}},r.a.createElement(W.a,null))),r.a.createElement(L.a,{open:t,anchorEl:l.current,transition:!0,disablePortal:!0},(function(e){var a=e.TransitionProps,t=e.placement;return r.a.createElement(N.a,Object.assign({},a,{style:{transformOrigin:"bottom"===t?"center top":"center bottom"}}),r.a.createElement(R.a,{id:"menu-list-grow"},r.a.createElement(F.a,{onClickAway:s},r.a.createElement(z.a,null,G.map((function(e,a){return r.a.createElement(T.a,{key:e,disabled:2===a,selected:a===i,onClick:function(e){return function(e,a){B(0===a),m(a),n(!1)}(0,a)}},e)}))))))})))},Q=Object(v.a)((function(e){return{appBar:Object(f.a)({marginLeft:240},e.breakpoints.up("sm"),{width:"calc(100% - ".concat(240,"px)")}),menuButton:{marginRight:e.spacing(2)},title:{flexGrow:1},logoutButton:{float:"right"}}}));var X=function(e){var a=e.handleMenuToggle,t=void 0===a?function(){}:a,n=Q(),l=Object(y.a)(),o=Object(k.a)(l.breakpoints.up("sm")),c=r.a.useContext(x),i=r.a.useState(!1),m=Object(u.a)(i,2),f=m[0],v=m[1];return f?(C.a.post("".concat(P,"/auth/logout"),{token:c}).then((function(e){console.log(e)})).catch((function(e){console.error(e)})),localStorage.removeItem("token"),r.a.createElement(d.a,{to:"/login"})):r.a.createElement(p.a,{position:"fixed",className:n.appBar},r.a.createElement(E.a,null,!o&&r.a.createElement(r.a.Fragment,null,r.a.createElement(g.a,{color:"inherit","aria-label":"open drawer",edge:"start",onClick:t,className:n.menuButton},r.a.createElement(O.a,null)),r.a.createElement(s.b,{to:"/",style:{color:"white",textDecoration:"none"}},r.a.createElement(h.a,{variant:"h5",noWrap:!0},"Slackr"))),r.a.createElement("div",{variant:"h6",className:n.title}),r.a.createElement("div",{style:{display:"flex"}},r.a.createElement($,null),r.a.createElement(b.a,{color:"inherit",className:n.logoutButton,onClick:function(){v(!0)}},"Logout"))))},Y=t(250),Z=t(252),ee=t(227);function ae(e,a){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);a&&(n=n.filter((function(a){return Object.getOwnPropertyDescriptor(e,a).enumerable}))),t.push.apply(t,n)}return t}function te(e){for(var a=1;a<arguments.length;a++){var t=null!=arguments[a]?arguments[a]:{};a%2?ae(t,!0).forEach((function(a){Object(f.a)(e,a,t[a])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):ae(t).forEach((function(a){Object.defineProperty(e,a,Object.getOwnPropertyDescriptor(t,a))}))}return e}var ne=Object(v.a)((function(e){return{drawer:Object(f.a)({},e.breakpoints.up("sm"),{width:240,flexShrink:0}),drawerPaper:{width:240},toolbar:te({},e.mixins.toolbar,{display:"flex",alignItems:"center",paddingLeft:e.spacing(2)})}}));var re=function(e){var a=e.container,t=e.children,n=e.open,l=e.setOpen,o=ne(),c=Object(y.a)();return r.a.createElement("nav",{className:o.drawer,"aria-label":"channels"},r.a.createElement(Y.a,{smUp:!0,implementation:"css"},r.a.createElement(Z.a,{container:a,variant:"temporary",anchor:"rtl"===c.direction?"right":"left",open:n,onClose:function(){return l(!1)},classes:{paper:o.drawerPaper},ModalProps:{keepMounted:!0}},r.a.createElement("div",{className:o.toolbar}),r.a.createElement(ee.a,null),t)),r.a.createElement(Y.a,{xsDown:!0,implementation:"css"},r.a.createElement(Z.a,{classes:{paper:o.drawerPaper},variant:"permanent",open:!0},r.a.createElement("div",{className:o.toolbar},r.a.createElement(s.b,{to:"/",style:{color:"black",textDecoration:"none"}},r.a.createElement(h.a,{variant:"h5",noWrap:!0},"Slackr"))),t)))},le=Object(v.a)((function(e){var a;return{body:(a={},Object(f.a)(a,e.breakpoints.up("sm"),{width:"calc(100% - ".concat(240,"px)")}),Object(f.a)(a,"padding",20),a),toolbar:e.mixins.toolbar}}));var oe=function(e){var a=e.children,t=le();return r.a.createElement("div",{className:t.body},r.a.createElement("div",{className:t.toolbar}),a)};var ce=function(e){var a=e.menu,t=e.body,n=r.a.useState(!1),l=Object(u.a)(n,2),o=l[0],c=l[1];return r.a.createElement("div",{style:{display:"flex"}},r.a.createElement(X,{handleMenuToggle:function(){c((function(e){return!e}))}}),r.a.createElement(re,{open:o,setOpen:c},a),r.a.createElement(oe,null,t))},ie=t(188),me=t(189),ue=t(228),se=t(229),de=t(104),fe=t.n(de);var pe=function(){var e=(r.a.useContext(x),0);return r.a.createElement(ie.a,null,r.a.createElement(me.a,{button:!0,key:"profile",component:s.b,to:"/profile/".concat(e)},r.a.createElement(ue.a,null,r.a.createElement(fe.a,null)),r.a.createElement(se.a,{primary:"Profile"})))},Ee=t(238),ge=t(73),he=t.n(ge),be=t(74),ve=t.n(be),ye=t(105),ke=t(230),_e=t(231),Oe=t(232),we=t(233),Ce=t(234),je=t(248),Se=t(236),xe=t(253),Pe=t(237),Ie=t(109),De=t.n(Ie),We=t(110),Fe=t.n(We),Ne=t(108),Re=t.n(Ne),Le="An error occured. Try again later",Te="Unable to retrieve channel information";var ze=function(e){Object(ye.a)({},e);var a=r.a.useState(!1),t=Object(u.a)(a,2),n=t[0],l=t[1],o=r.a.useContext(x);function c(){l(!1)}return r.a.createElement("div",null,r.a.createElement(g.a,{size:"small",onClick:function(){l(!0)}},r.a.createElement(Re.a,null)),r.a.createElement(ke.a,{open:n,onClose:c,"aria-labelledby":"form-dialog-title"},r.a.createElement(_e.a,{id:"form-dialog-title"},"Create Channel"),r.a.createElement("form",{onSubmit:function(e){e.preventDefault();var a=e.target[0].value,t=!e.target[1].checked;console.log(t),a&&C.a.post("".concat(P,"/channel/create"),{token:o,channel_name:a,is_public:t}).then((function(e){console.log(e)})).catch((function(e){console.error(e),m.b.error(Le)}))}},r.a.createElement(Oe.a,null,r.a.createElement(we.a,null,"Complete the form below to create a new channel"),r.a.createElement(Ce.a,{container:!0,spacing:2,direction:"row",justify:"center",alignItems:"center"},r.a.createElement(Ce.a,{item:!0,xs:12},r.a.createElement(je.a,{autoFocus:!0,margin:"dense",id:"channel_name",label:"Channel Name",name:"channel_name",fullWidth:!0})),r.a.createElement(Ce.a,{container:!0,item:!0,justify:"center",alignItems:"center"},r.a.createElement(De.a,null),r.a.createElement(Se.a,{control:r.a.createElement(xe.a,{value:"secret",inputProps:{"aria-label":"Secret"}}),label:"Secret",labelPlacement:"top"}),r.a.createElement(Fe.a,null)))),r.a.createElement(Pe.a,null,r.a.createElement(b.a,{onClick:c,color:"primary"},"Cancel"),r.a.createElement(b.a,{onClick:c,type:"submit",color:"primary"},"Create")))))};var Ve=function(e){var a=e.channel_id,t=r.a.useState([]),n=Object(u.a)(t,2),l=n[0],o=n[1],c=r.a.useState([]),i=Object(u.a)(c,2),m=i[0],d=i[1],f=r.a.useContext(x);return r.a.useEffect((function(){C.a.all([C.a.get("".concat(P,"/channels/list"),{params:{token:f}}),C.a.get("".concat(P,"/channels/listall"),{params:{token:f}})]).then(C.a.spread((function(e,a){var t=e.data.channels;console.log(t);var n=a.data.channels.filter((function(e){return void 0===t.find((function(a){return a.channel_id===e.channel_id}))}));console.log(n),o(t),d(n)})))}),[]),r.a.createElement(r.a.Fragment,null,r.a.createElement(ie.a,{subheader:r.a.createElement(Ee.a,{style:{display:"flex"}},r.a.createElement("span",{style:{flex:1}},"My Channels"),r.a.createElement(ze,null))},l.map((function(e,t){var n=e.channel_id,l=e.name;return r.a.createElement(me.a,{button:!0,key:n,component:s.b,to:"/channel/".concat(n)},r.a.createElement(ue.a,null,n==a?r.a.createElement(he.a,null):r.a.createElement(ve.a,null)),r.a.createElement(se.a,{primary:l}))}))),r.a.createElement(ie.a,{subheader:r.a.createElement(Ee.a,null,"Other Channels")},m.map((function(e,t){var n=e.channel_id,l=e.name;return r.a.createElement(me.a,{button:!0,key:n,component:s.b,to:"/channel/".concat(n)},r.a.createElement(ue.a,null,n==a?r.a.createElement(he.a,null):r.a.createElement(ve.a,null)),r.a.createElement(se.a,{primary:l}))}))))};var Ae=function(e){var a=e.channel_id;return r.a.createElement(r.a.Fragment,null,r.a.createElement(pe,null),r.a.createElement(Ve,{channel_id:a}))};var qe=function(e){return r.a.createElement(ce,{menu:r.a.createElement(Ae,null),body:r.a.createElement(r.a.Fragment,null,r.a.createElement(h.a,{variant:"h4"},"WELCOME"),r.a.createElement("div",{style:{paddingTop:15}},r.a.createElement(h.a,{variant:"body1"},"This is SengChat: agile messaging for Software Engineers \u2764\ufe0f")))})},Be=t(25),Me=t(241),Ue=t(243),Je=t(120),He=t.n(Je),Ke=t(119),Ge=t.n(Ke);var $e=function(e){var a=e.channel_id,t=(Object(Be.a)(e,["channel_id"]),r.a.useState(!1)),n=Object(u.a)(t,2),l=n[0],o=n[1],c=r.a.useContext(x);function i(){o(!1)}return r.a.createElement("div",null,r.a.createElement(b.a,{variant:"outlined",color:"primary",onClick:function(){o(!0)}},"Invite Member"),r.a.createElement(ke.a,{open:l,onClose:i,"aria-labelledby":"form-dialog-title"},r.a.createElement(_e.a,{id:"form-dialog-title"},"Invite User"),r.a.createElement("form",{onSubmit:function(e){e.preventDefault();var t=e.target[0].value;t&&C.a.post("".concat(P,"/channel/invite"),{token:c,user_id:t,channel_id:a}).then((function(e){console.log(e)})).catch((function(e){console.error(e),m.b.error(Le)}))}},r.a.createElement(Oe.a,null,r.a.createElement(we.a,null,"Enter a user id below to invite a user to this channel"),r.a.createElement(je.a,{autoFocus:!0,margin:"dense",id:"user_id",label:"User ID",name:"user_id",fullWidth:!0})),r.a.createElement(Pe.a,null,r.a.createElement(b.a,{onClick:i,color:"primary"},"Cancel"),r.a.createElement(b.a,{onClick:i,type:"submit",color:"primary"},"Invite")))))},Qe=t(111),Xe=t.n(Qe),Ye=t(75),Ze=t.n(Ye),ea=t(76),aa=t(239);var ta=Object(aa.a)((function(e){var a=e.message_id,t=e.is_pinned,n=void 0!==t&&t,l=e.theme,o=r.a.useState(n),c=Object(u.a)(o,2),i=c[0],m=c[1];r.a.useEffect((function(){return m(n)}),[n]);var s=r.a.useContext(x);return r.a.createElement(g.a,{onClick:function(){i?C.a.post("".concat(P,"/message/unpin"),{token:s,message_id:a}):C.a.post("".concat(P,"/message/pin"),{token:s,message_id:a})},style:{margin:1},size:"small",edge:"end","aria-label":"delete"},i?r.a.createElement(Ze.a,{path:ea.a,size:"1em",color:l&&l.palette.action.active}):r.a.createElement(Ze.a,{path:ea.b,size:"1em",color:l&&l.palette.action.active}))})),na=t(240),ra=t(112),la=t.n(ra),oa=t(113),ca=t.n(oa);var ia=function(e){var a=e.message_id,t=e.reacts,n=void 0===t?[]:t,l=r.a.useContext(x),o=0,c=!1,i=n.findIndex((function(e){return 1===e.react_id}));return-1!==i&&(o=n[i].u_ids.length,c=n[i].is_this_user_reacted),r.a.createElement(na.a,{anchorOrigin:{horizontal:"right",vertical:"bottom"},badgeContent:o,color:"secondary"},r.a.createElement(g.a,{onClick:function(){return function(e){e?C.a.post("".concat(P,"/message/unreact"),{token:l,message_id:a,react_id:1}):C.a.post("".concat(P,"/message/react"),{token:l,message_id:a,react_id:1})}(c)},style:{margin:1},size:"small",edge:"end","aria-label":"delete"},c?r.a.createElement(la.a,{fontSize:"small"}):r.a.createElement(ca.a,{fontSize:"small"})))},ma=t(114),ua=t.n(ma);var sa=function(e){var a=e.message_id,t=r.a.useContext(x);return r.a.createElement(g.a,{onClick:function(){C.a.post("".concat(P,"/message/remove"),{token:t,message_id:a})},style:{margin:1},size:"small",edge:"end","aria-label":"delete"},r.a.createElement(ua.a,{fontSize:"small"}))};var da=function(e){var a=e.message_id,t=e.message,n=void 0===t?"":t,l=e.u_id,o=e.time_created,c=(e.is_unread,e.is_pinned),i=void 0!==c&&c,m=e.reacts,s=void 0===m?[]:m,d=r.a.useState(),f=Object(u.a)(d,2),p=f[0],E=f[1],g=r.a.useState(),h=Object(u.a)(g,2),b=h[0],v=h[1],y=r.a.useContext(x);return r.a.useEffect((function(){E(),v(),C.a.get("".concat(P,"/user/profile"),{params:{token:y,u_id:l}}).then((function(e){var a=e.data,t=(a.email,a.name_first),n=void 0===t?"":t,r=a.name_last,l=void 0===r?"":r;a.handle_str;E("".concat(n," ").concat(l)),v("".concat(n[0]).concat(l[0]))})).catch((function(e){console.error(e)}))}),[a,y,l]),r.a.createElement(me.a,{key:a,style:{width:"100%"}},p&&b&&n&&r.a.createElement(r.a.Fragment,null,r.a.createElement(ue.a,null,r.a.createElement(Me.a,null,b)),r.a.createElement("div",{style:{display:"flex",width:"100%",justifyContent:"space-between",alignItems:"center"}},r.a.createElement(se.a,{primary:r.a.createElement(r.a.Fragment,null,r.a.createElement("span",null,p),r.a.createElement("span",{style:{paddingLeft:10,fontSize:10}},Xe()(1e3*o))),secondary:n}),r.a.createElement("div",{style:{display:"flex",height:30,marginLeft:20}},r.a.createElement(ia,{message_id:a,reacts:s,u_id:l}),r.a.createElement(ta,{message_id:a,is_pinned:i}),r.a.createElement(sa,{message_id:a})))))},fa=t(242),pa=t(118),Ea=t.n(pa),ga=t(117),ha=t.n(ga),ba=t(191),va=t(247);var ya=function(e){var a=e.open,t=e.handleClose,n=e.onTimerChange,l=(Object(Be.a)(e,["open","handleClose","onTimerChange"]),r.a.useState(new Date)),o=Object(u.a)(l,2),c=o[0],i=o[1];return r.a.createElement("div",null,r.a.createElement(ke.a,{open:a,onClose:t,"aria-labelledby":"form-dialog-title"},r.a.createElement(_e.a,{id:"form-dialog-title"},"Send later"),r.a.createElement("form",{onSubmit:function(e){e.preventDefault(),n(c)}},r.a.createElement(Oe.a,null,r.a.createElement(va.a,{margin:"normal",id:"time-picker",label:"Time picker",value:c,onChange:function(e){return i(e.toDate())},KeyboardButtonProps:{"aria-label":"change time"}}),r.a.createElement(we.a,null,"Enter a time to send")),r.a.createElement(Pe.a,null,r.a.createElement(b.a,{onClick:t,color:"primary"},"Cancel"),r.a.createElement(b.a,{onClick:t,type:"submit",color:"primary"},"Set Time")))))},ka=Object(ba.a)((function(e){return{flex:{display:"flex",flexDirection:"row",alignItems:"center"},input:{margin:e.spacing(1),marginRight:0},button:{margin:e.spacing(1),marginLeft:0,alignSelf:"stretch"},rightIcon:{marginLeft:e.spacing(1)}}})),_a=-1;var Oa=function(e){var a=e.channel_id,t=void 0===a?"":a,n=ka(),l=r.a.useState(""),o=Object(u.a)(l,2),c=o[0],i=o[1],s=r.a.useState(_a),d=Object(u.a)(s,2),f=d[0],p=d[1],E=r.a.useState(!1),h=Object(u.a)(E,2),v=h[0],y=h[1],k=r.a.useContext(x),_=f!==_a,O=function(){var e=c.trim();e&&(i(""),_?(C.a.post("".concat(P,"/message/sendlater"),{token:k,channel_id:t,message:e,time_sent:f.toISOString()}).then((function(e){var a=e.data;console.log(a)})).catch((function(e){console.error(e),m.b.error(Le)})),p(_a)):C.a.post("".concat(P,"/message/send"),{token:k,channel_id:t,message:e}).then((function(e){var a=e.data;console.log(a)})).catch((function(e){console.error(e),m.b.error(Le)})))};return r.a.createElement(r.a.Fragment,null,r.a.createElement("div",{className:n.flex},r.a.createElement(je.a,{className:n.input,label:"Send a message \ud83d\udcac",multiline:!0,placeholder:"...",fullWidth:!0,margin:"normal",variant:"filled",onKeyDown:function(e){"Enter"!==e.key||e.getModifierState("Shift")||(e.preventDefault(),O())},value:c,onChange:function(e){return i(e.target.value)},InputProps:{endAdornment:r.a.createElement(fa.a,{position:"end"},r.a.createElement(g.a,{"aria-label":"toggle visibility",onClick:function(){return _?p(-1):y(!0)}},r.a.createElement(ha.a,{color:_?"secondary":void 0})))}}),r.a.createElement(b.a,{className:n.button,variant:"contained",color:"primary",onClick:O},"Send",r.a.createElement(Ea.a,{className:n.rightIcon}))),r.a.createElement(ya,{open:v,handleClose:function(){return y(!1)},onTimerChange:p}))};var wa=function(e){var a=e.channel_id,t=void 0===a?"":a,l=r.a.useState([]),o=Object(u.a)(l,2),c=o[0],i=o[1],s=r.a.useState(0),d=Object(u.a)(s,2),f=d[0],p=d[1],E=r.a.useContext(x),g=function(){return C.a.get("".concat(P,"/channel/messages"),{params:{token:E,channel_id:t,start:f}}).then((function(e){var a=e.data,t=a.messages,n=(a.start,a.end);p(n),i(t)})).catch((function(e){console.error(e),m.b.error(Te)}))};return r.a.useEffect((function(){return J(g),function(){return H(g)}}),[]),function(e,a){var t=Object(n.useRef)();Object(n.useEffect)((function(){t.current=e}),[e]),Object(n.useEffect)((function(){if(null!==a){var e=setInterval((function(){t.current()}),a);return function(){return clearInterval(e)}}}),[a])}((function(){q()&&g()}),M),r.a.useEffect((function(){C.a.get("".concat(P,"/channel/messages"),{params:{token:E,channel_id:t,start:f}}).then((function(e){var a=e.data,t=a.messages,n=(a.start,a.end);p(n),i(t)})).catch((function(e){console.error(e),m.b.error(Te)}))}),[E,t,f]),r.a.createElement(r.a.Fragment,null,r.a.createElement(ie.a,{subheader:r.a.createElement(Ee.a,null,"Messages"),style:{width:"100%"}},c.map((function(e){return r.a.createElement(da,e)}))),r.a.createElement(Oa,{channel_id:t}))};var Ca=function(e){var a=e.channel_id,t=(Object(Be.a)(e,["channel_id"]),r.a.useState("")),n=Object(u.a)(t,2),l=n[0],o=n[1],c=r.a.useState([]),i=Object(u.a)(c,2),s=i[0],d=i[1],f=r.a.useState([]),p=Object(u.a)(f,2),E=p[0],v=p[1],y=r.a.useContext(x),k=0;function _(e,a){C.a.get("".concat(P,"/channel/details"),{params:{token:a,channel_id:e}}).then((function(e){var a=e.data;console.log(a);var t=a.name,n=a.owner_members,r=a.all_members;d(r),v(n),o(t)})).catch((function(e){console.error(e),m.b.error(Te)}))}function O(e,a){return void 0!==e.find((function(e){return e.u_id===a}))}r.a.useEffect((function(){_(a,y)}),[a,y]);var w=O(E,k);return r.a.createElement(r.a.Fragment,null,r.a.createElement(h.a,{variant:"h4"},l.toUpperCase()),r.a.createElement(ie.a,{subheader:r.a.createElement(Ee.a,null,"Members")},s.map((function(e){var t=e.u_id,n=e.name_first,l=e.name_last;return r.a.createElement(me.a,{key:t},r.a.createElement(ue.a,null,r.a.createElement(Me.a,null,n[0],l[0])),r.a.createElement(se.a,{primary:r.a.createElement(r.a.Fragment,null,r.a.createElement(Ce.a,{container:!0,alignItems:"center",spacing:1},r.a.createElement(Ce.a,{item:!0},r.a.createElement(Ue.a,{href:"/profile/".concat(t)},"".concat(n," ").concat(l)),"".concat(O(E,t)?" \u2b50":" ")),w&&r.a.createElement(Ce.a,{item:!0},O(E,t)?r.a.createElement(g.a,{size:"small",onClick:function(){return function(e){C.a.post("".concat(P,"/channel/removeowner"),{token:y,channel_id:a,u_id:e}).then((function(){_(a,y)})).catch((function(e){console.error(e),m.b.error(Le)}))}(t)}},r.a.createElement(Ge.a,null)):r.a.createElement(g.a,{size:"small",onClick:function(){return function(e){C.a.post("".concat(P,"/channel/addowner"),{token:y,channel_id:a,u_id:e}).then((function(){_(a,y)})).catch((function(e){console.error(e),m.b.error(Le)}))}(t)}},r.a.createElement(He.a,null)))))}))})),r.a.createElement(me.a,{key:"invite_member"},function(e){return console.log(e),void 0!==e.find((function(e){return e.u_id===k}))}(s)?r.a.createElement(Ce.a,{container:!0,spacing:1},r.a.createElement(Ce.a,{item:!0},r.a.createElement($e,{channel_id:a})),r.a.createElement(Ce.a,{item:!0},r.a.createElement(b.a,{variant:"outlined",onClick:function(){return function(e,a){C.a.post("".concat(P,"/channel/leave"),{token:a,channel_id:e}).then((function(){_(e,a)})).catch((function(e){console.error(e),m.b.error(Le)}))}(a,y)}},"Leave Channel"))):r.a.createElement(b.a,{variant:"outlined",color:"primary",onClick:function(){return function(e,a){C.a.post("".concat(P,"/channel/join"),{token:a,channel_id:e}).then((function(){_(e,a)})).catch((function(e){console.error(e),m.b.error(Le)}))}(a,y)}},"Join Channel"))),r.a.createElement(wa,{channel_id:a}))};var ja=function(e){var a=e.match.params.channel_id;return r.a.createElement(ce,{menu:r.a.createElement(Ae,{channel_id:a}),body:r.a.createElement(Ca,{channel_id:a})})},Sa=t(244),xa=t(249),Pa=t(121),Ia=t.n(Pa),Da=Object(v.a)((function(e){return{"@global":{body:{backgroundColor:e.palette.primary.light}},card:{backgroundColor:e.palette.background.paper,marginTop:e.spacing(8),padding:e.spacing(8),display:"flex",flexDirection:"column",alignItems:"center",borderRadius:e.shape.borderRadius}}}));var Wa=function(e){var a=e.setAuth,t=Object(Be.a)(e,["setAuth"]),n=Da();return r.a.createElement(Sa.a,{component:"main",maxWidth:"sm"},r.a.createElement(xa.a,{boxShadow:3,className:n.card},r.a.createElement(Me.a,null,r.a.createElement(Ia.a,null)),r.a.createElement(h.a,{component:"h1",variant:"h5"},"Login"),r.a.createElement("form",{noValidate:!0,onSubmit:function(e){e.preventDefault();var n=e.target[0].value,r=e.target[2].value;n&&r&&C.a.post("".concat(P,"/auth/login"),{handle:n,password:r}).then((function(e){console.log(e);var n=e.data;a(n.token),t.history.push("/")})).catch((function(e){console.error(e),m.b.error(Le)}))}},r.a.createElement(je.a,{variant:"outlined",margin:"normal",required:!0,fullWidth:!0,id:"email",label:"Email",name:"email",type:"text",autoFocus:!0}),r.a.createElement(je.a,{variant:"outlined",margin:"normal",required:!0,fullWidth:!0,name:"password",label:"Password",type:"password",id:"password",autoComplete:"current-password"}),r.a.createElement(b.a,{type:"submit",fullWidth:!0,variant:"contained",color:"primary"},"Sign In"),r.a.createElement(Ce.a,{container:!0,direction:"column",alignItems:"center"},r.a.createElement(Ce.a,{item:!0},r.a.createElement("br",null),r.a.createElement(Ue.a,{href:"/register",variant:"body1"},"Don't have an account? Register")),r.a.createElement(Ce.a,{item:!0},r.a.createElement("br",null),r.a.createElement(Ue.a,{href:"/forgot_password",variant:"body1"},"Forgot password?"))))))},Fa=t(55),Na=t.n(Fa),Ra=Object(v.a)((function(e){return{"@global":{body:{backgroundColor:e.palette.primary.light}},card:{backgroundColor:e.palette.background.paper,marginTop:e.spacing(8),padding:e.spacing(8),display:"flex",flexDirection:"column",alignItems:"center",borderRadius:e.shape.borderRadius}}}));var La=function(e){var a=e.setAuth,t=Object(Be.a)(e,["setAuth"]),n=Ra();return r.a.createElement(Sa.a,{component:"main",maxWidth:"sm"},r.a.createElement(xa.a,{boxShadow:3,className:n.card},r.a.createElement(Me.a,null,r.a.createElement(Na.a,{color:"secondary"})),r.a.createElement(h.a,{component:"h1",variant:"h5"},"Register"),r.a.createElement("form",{noValidate:!0,onSubmit:function(e){e.preventDefault();var n=e.target[0].value,r=e.target[2].value,l=e.target[4].value;r&&l&&C.a.post("".concat(P,"/auth/register"),{name:n,handle:r,password:l}).then((function(e){console.log(e);var n=e.data;a(n),t.history.push("/")})).catch((function(e){console.error(e),m.b.error(Le)}))}},r.a.createElement(je.a,{variant:"outlined",margin:"normal",required:!0,fullWidth:!0,id:"name_first",label:"Firstname",name:"name_first",type:"text",autoFocus:!0}),r.a.createElement(je.a,{variant:"outlined",margin:"normal",required:!0,fullWidth:!0,id:"name_last",label:"Lastname",name:"name_last",type:"text",autoFocus:!0}),r.a.createElement(je.a,{variant:"outlined",margin:"normal",required:!0,fullWidth:!0,id:"email",label:"Email",name:"email",type:"email"}),r.a.createElement(je.a,{variant:"outlined",margin:"normal",required:!0,fullWidth:!0,name:"password",label:"Password",type:"password",id:"password",autoComplete:"current-password"}),r.a.createElement(b.a,{type:"submit",fullWidth:!0,variant:"contained",color:"primary"},"Sign Up"),r.a.createElement(Ce.a,{container:!0},r.a.createElement(Ce.a,{item:!0},r.a.createElement("br",null),r.a.createElement(Ue.a,{href:"/login",variant:"body1"},"Already have an account? Login"))))))},Ta=Object(v.a)((function(e){return{"@global":{body:{backgroundColor:e.palette.primary.light}},card:{backgroundColor:e.palette.background.paper,marginTop:e.spacing(8),padding:e.spacing(8),display:"flex",flexDirection:"column",alignItems:"center",borderRadius:e.shape.borderRadius}}}));var za=function(e){var a=Ta();return r.a.createElement(Sa.a,{component:"main",maxWidth:"sm"},r.a.createElement(xa.a,{boxShadow:3,className:a.card},r.a.createElement(Me.a,null,r.a.createElement(Na.a,{color:"secondary"})),r.a.createElement(h.a,{component:"h1",variant:"h5"},"Forgot Password"),r.a.createElement("form",{noValidate:!0,onSubmit:function(a){a.preventDefault();var t=a.target[0].value;t&&C.a.post("".concat(P,"/auth/passwordreset/request"),{email:t}).then((function(a){console.log(a),e.history.push("/reset_password")})).catch((function(e){console.error(e),m.b.error(Le)}))}},r.a.createElement(je.a,{variant:"outlined",margin:"normal",required:!0,fullWidth:!0,id:"email",label:"Email",name:"email",type:"email",autoFocus:!0}),r.a.createElement(b.a,{type:"submit",fullWidth:!0,variant:"contained",color:"primary"},"Send Recovery Email"),r.a.createElement(Ce.a,{container:!0},r.a.createElement(Ce.a,{item:!0},r.a.createElement("br",null),r.a.createElement(Ue.a,{href:"/login",variant:"body1"},"Remember your password? Login"))))))},Va=Object(v.a)((function(e){return{"@global":{body:{backgroundColor:e.palette.primary.light}},card:{backgroundColor:e.palette.background.paper,marginTop:e.spacing(8),padding:e.spacing(8),display:"flex",flexDirection:"column",alignItems:"center",borderRadius:e.shape.borderRadius}}}));var Aa=function(e){var a=Va();return r.a.createElement(Sa.a,{component:"main",maxWidth:"sm"},r.a.createElement(xa.a,{boxShadow:3,className:a.card},r.a.createElement(Me.a,null,r.a.createElement(Na.a,{color:"secondary"})),r.a.createElement(h.a,{component:"h1",variant:"h5"},"Reset Password"),r.a.createElement("form",{noValidate:!0,onSubmit:function(a){a.preventDefault();var t=a.target[0].value,n=a.target[2].value;t&&n&&C.a.post("".concat(P,"/auth/passwordreset/reset"),{reset_code:t,new_password:n}).then((function(a){console.log(a),e.history.push("/login")})).catch((function(e){console.error(e),m.b.error(Le)}))}},r.a.createElement(je.a,{variant:"outlined",margin:"normal",required:!0,fullWidth:!0,id:"reset_code",label:"Reset code",name:"reset_code",type:"text",autoFocus:!0}),r.a.createElement(je.a,{variant:"outlined",margin:"normal",required:!0,fullWidth:!0,id:"new_password",label:"New Password",name:"new_password",type:"password"}),r.a.createElement(b.a,{type:"submit",fullWidth:!0,variant:"contained",color:"primary"},"Change Password"),r.a.createElement(Ce.a,{container:!0},r.a.createElement(Ce.a,{item:!0},r.a.createElement("br",null),r.a.createElement(Ue.a,{href:"/login",variant:"body1"},"Remember your password? Login"))))))},qa=t(128),Ba=t(124),Ma=t.n(Ba),Ua=t(123),Ja=t.n(Ua),Ha=t(122),Ka=t.n(Ha);var Ga=function(e){var a=e.editable,t=e.master,n=e.masterValue,l=e.slaves,o=e.slaveValues,c=e.onSave,i=(Object(Be.a)(e,["editable","master","masterValue","slaves","slaveValues","onSave"]),r.a.useState(!1)),m=Object(u.a)(i,2),s=m[0],d=m[1],f=r.a.useState(),p=Object(u.a)(f,2),E=p[0],g=p[1],h=r.a.useState(n),b=Object(u.a)(h,2),v=b[0],y=b[1],k=r.a.useState([]),_=Object(u.a)(k,2),O=_[0],w=_[1],C=r.a.useState(o),j=Object(u.a)(C,2),S=j[0],x=j[1];function P(){g(v),w(S),d(!s)}return r.a.createElement(Ce.a,{container:!0,spacing:1,alignItems:"flex-end"},l&&l.map((function(e,a){return r.a.createElement(Ce.a,{item:!0,key:a},e({value:S[a],InputProps:{readOnly:!s},onChange:function(e){return function(e,a){var t=S.map((function(t,n){return n===a?e.target.value:t}));x(t)}(e,a)}}))})),r.a.createElement(Ce.a,{item:!0},t({value:v,InputProps:{readOnly:!s},onChange:function(e){y(e.target.value)}})),a&&r.a.createElement(Ce.a,{item:!0},a?s?r.a.createElement(r.a.Fragment,null,r.a.createElement(Ka.a,{style:{cursor:"pointer"},onClick:function(){v&&(c&&(S?c.apply(void 0,[v].concat(Object(qa.a)(S))):c(v)),P())}}),r.a.createElement(Ja.a,{style:{cursor:"pointer"},onClick:function(){y(E),x(O),P()}})):r.a.createElement(Ma.a,{style:{cursor:"pointer"},onClick:P}):null))};var $a=function(e){var a=e.profile,t=(Object(Be.a)(e,["profile"]),r.a.useState({})),n=Object(u.a)(t,2),l=n[0],o=n[1],c=r.a.useContext(x),i=0;r.a.useEffect((function(){C.a.get("".concat(P,"/user/profile"),{params:{token:c,profile:a}}).then((function(e){var a=e.data;console.log(a),o(a)})).catch((function(e){console.error(e)}))}),[a,c]);var m=i.toString()===a;return r.a.createElement(r.a.Fragment,null,r.a.createElement(h.a,{variant:"h4"},"Profile"),r.a.createElement(ie.a,{subheader:r.a.createElement(Ee.a,null,"Profile Details")},r.a.createElement(me.a,{key:"name"},r.a.createElement(Ga,{editable:m,masterValue:l.last_name,slaveValues:[l.first_name],master:function(e){return r.a.createElement(je.a,Object.assign({label:"Last Name"},e))},slaves:[function(e){return r.a.createElement(je.a,Object.assign({label:"First Name"},e))}],onSave:function(e,a){C.a.put("".concat(P,"/user/profile/setname"),{token:c,name_first:a,name_last:e}).then((function(){console.log("all good")})).catch((function(e){console.error(e)}))}})),r.a.createElement(me.a,{key:"email"},r.a.createElement(Ga,{editable:m,masterValue:l.email,master:function(e){return r.a.createElement(je.a,Object.assign({label:"Email"},e))},onSave:function(e){C.a.put("".concat(P,"/user/profile/setemail"),{token:c,email:e}).then((function(){console.log("all good")})).catch((function(e){console.error(e)}))}})),r.a.createElement(me.a,{key:"handle"},r.a.createElement(Ga,{editable:m,masterValue:"phlips",master:function(e){return r.a.createElement(je.a,Object.assign({label:"Handle"},e))},onSave:function(e){C.a.put("".concat(P,"/user/profile/sethandle"),{token:c,handle:e}).then((function(){console.log("all good")})).catch((function(e){console.error(e)}))}}))))};var Qa=function(e){var a=e.match.params.profile;return r.a.createElement(ce,{menu:r.a.createElement(Ae,null),body:r.a.createElement($a,{profile:a})})};var Xa=function(e){var a=r.a.useContext(x);return console.log(a),a?r.a.createElement(d.b,e):r.a.createElement(d.a,{to:"/login"})};var Ya=function(){var e=r.a.useState(localStorage.getItem("token")),a=Object(u.a)(e,2),t=a[0],n=a[1];function l(e){localStorage.setItem("token",e),n(e)}return r.a.createElement(S,{value:t},r.a.createElement(s.a,null,r.a.createElement(d.d,null,r.a.createElement(d.b,{exact:!0,path:"/login",render:function(e){return r.a.createElement(Wa,Object.assign({},e,{setAuth:l}))}}),r.a.createElement(d.b,{exact:!0,path:"/register",render:function(e){return r.a.createElement(La,Object.assign({},e,{setAuth:l}))}}),r.a.createElement(d.b,{exact:!0,path:"/forgot_password",component:za}),r.a.createElement(d.b,{exact:!0,path:"/reset_password",component:Aa}),r.a.createElement(Xa,{exact:!0,path:"/",component:qe}),r.a.createElement(Xa,{path:"/profile/:profile",component:Qa}),r.a.createElement(Xa,{path:"/channel/:channel_id",component:ja}))))};Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));var Za=t(67),et=t(127),at=Object(et.a)({palette:{primary:{main:"#556cd6"},secondary:{main:"#19857b"},error:{main:Za.a.A400},background:{default:"#fff"}}}),tt=t(22),nt=t(125);o.a.render(r.a.createElement(i.a,{theme:at},r.a.createElement(tt.a,{utils:nt.a},r.a.createElement(c.a,null),r.a.createElement(Ya,null),r.a.createElement(m.a,{position:"top-center",autoClose:5e3,hideProgressBar:!1,newestOnTop:!0,closeOnClick:!0,rtl:!1,pauseOnVisibilityChange:!0,draggable:!0,pauseOnHover:!0}))),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()}))}},[[151,1,2]]]);
//# sourceMappingURL=main.f187e6d0.chunk.js.map