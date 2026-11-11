document.addEventListener("DOMContentLoaded",()=>{const inputs=[...document.querySelectorAll(".otp-inputs input")];inputs.forEach((input,i)=>{input.addEventListener("input",()=>{input.value=input.value.replace(/\D/g,"").slice(0,1);if(input.value&&inputs[i+1])inputs[i+1].focus()});input.addEventListener("keydown",e=>{if(e.key==="Backspace"&&!input.value&&inputs[i-1])inputs[i-1].focus()})});document.querySelectorAll(".colour-choice").forEach(button=>button.addEventListener("click",()=>{document.querySelectorAll(".colour-choice").forEach(b=>b.classList.remove("selected"));button.classList.add("selected")}));});

document.addEventListener("DOMContentLoaded",()=>{const menu=document.querySelector(".menu-toggle");const mobileNav=document.querySelector(".mobile-nav");if(menu&&mobileNav){menu.addEventListener("click",()=>{const open=document.body.classList.toggle("menu-open");menu.setAttribute("aria-expanded",String(open));menu.setAttribute("aria-label",open?"Close menu":"Open menu")});mobileNav.addEventListener("click",event=>{if(event.target.closest("a")){document.body.classList.remove("menu-open");menu.setAttribute("aria-expanded","false");menu.setAttribute("aria-label","Open menu")}});document.addEventListener("keydown",event=>{if(event.key==="Escape"){document.body.classList.remove("menu-open");menu.setAttribute("aria-expanded","false");menu.setAttribute("aria-label","Open menu")}})}const reveals=document.querySelectorAll("[data-reveal]");if("IntersectionObserver"in window){const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add("is-visible");observer.unobserve(entry.target)}}),{threshold:.12});reveals.forEach(item=>observer.observe(item))}else reveals.forEach(item=>item.classList.add("is-visible"));});

document.addEventListener("DOMContentLoaded",()=>{
  const main=document.querySelector("#campaign-main");
  const kids=document.querySelector("#campaign-kids");
  if(!main||!kids)return;
  const copies={main:document.querySelector(".campaign-copy--main"),kids:document.querySelector(".campaign-copy--kids")};
  const fallback=document.querySelector(".campaign-fallback");
  const controls=[...document.querySelectorAll("[data-campaign-slide]")];
  const playFromStart=video=>{
    const start=()=>{
      if(video.readyState>=1)video.currentTime=0;
      const attempt=video.play();
      if(attempt&&attempt.catch)attempt.catch(()=>{
        video.addEventListener("canplay",()=>video.play().catch(()=>{}),{once:true});
        video.load();
      });
    };
    if(video.readyState>=2)start();
    else{
      video.addEventListener("canplay",start,{once:true});
      video.load();
    }
  };
  const activate=(slide,play=true)=>{
    const showKids=slide==="kids";
    main.classList.toggle("is-active",!showKids);
    kids.classList.toggle("is-active",showKids);
    copies.main.classList.toggle("is-active",!showKids);
    copies.kids.classList.toggle("is-active",showKids);
    controls.forEach(button=>button.classList.toggle("is-active",button.dataset.campaignSlide===slide));
    fallback.src=showKids?fallback.dataset.kidsPoster:fallback.dataset.mainPoster;
    main.pause();kids.pause();
    if(play)playFromStart(showKids?kids:main);
  };
  fallback.dataset.mainPoster=fallback.src;
  main.addEventListener("ended",()=>activate("kids"));
  kids.addEventListener("ended",()=>activate("main"));
  controls.forEach(button=>button.addEventListener("click",()=>activate(button.dataset.campaignSlide)));
});

document.addEventListener("DOMContentLoaded",()=>{const previews=document.querySelectorAll("[data-video-preview]");if(!previews.length)return;const reducedMotion=window.matchMedia("(prefers-reduced-motion: reduce)").matches;if(reducedMotion)return;if("IntersectionObserver"in window){const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{const video=entry.target;if(entry.isIntersecting){const play=video.play();if(play&&play.catch)play.catch(()=>{})}else video.pause()}),{threshold:.25});previews.forEach(video=>observer.observe(video))}else previews.forEach(video=>{const play=video.play();if(play&&play.catch)play.catch(()=>{})});});
