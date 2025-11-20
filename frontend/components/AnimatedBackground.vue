<template>
  <div class="animated-background">
    <!-- Background Image with Overlay -->
    <div class="absolute inset-0 z-0">
      <img src="/loginbackgrpound.png" alt="Hotel Background" class="w-full h-full object-cover" />
      <div class="absolute inset-0 bg-gradient-to-br from-blue-900/80 via-purple-900/70 to-indigo-900/80 backdrop-blur-sm"></div>
    </div>

    <!-- Floating Elements - Images -->
    <div class="floating-element absolute top-20 left-10 w-24 h-24 opacity-25">
      <img src="/cartoon.png" alt="Hotel Icon" class="w-full h-full object-contain animate-float drop-shadow-lg" />
    </div>
    <div class="floating-element absolute top-40 right-20 w-32 h-32 opacity-20">
      <img src="/rec2.png" alt="Hotel Icon" class="w-full h-full object-contain animate-float-delayed drop-shadow-xl" />
    </div>
    <div class="floating-element absolute bottom-32 left-20 w-36 h-36 opacity-15">
      <img src="/cartoon.png" alt="Hotel Icon" class="w-full h-full object-contain animate-float-slow drop-shadow-2xl" />
    </div>
    <div class="floating-element absolute bottom-20 right-32 w-28 h-28 opacity-25">
      <img src="/rec2.png" alt="Hotel Icon" class="w-full h-full object-contain animate-float drop-shadow-lg" />
    </div>
    <div class="floating-element absolute top-1/3 left-1/4 w-20 h-20 opacity-20">
      <img src="/cartoon.png" alt="Hotel Icon" class="w-full h-full object-contain animate-float-delayed drop-shadow-md" />
    </div>
    <div class="floating-element absolute bottom-1/3 right-1/4 w-24 h-24 opacity-15">
      <img src="/rec2.png" alt="Hotel Icon" class="w-full h-full object-contain animate-float-slow drop-shadow-lg" />
    </div>

    <!-- Floating SVG Icons -->
    <div class="absolute top-32 right-1/4 w-16 h-16 text-white/20 animate-float-slow">
      <svg fill="currentColor" viewBox="0 0 24 24" class="drop-shadow-lg">
        <path d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5zm0 2.18l8 4V17c0 4.52-3.15 8.72-8 10-4.85-1.28-8-5.48-8-10V8.18l8-4zM11 9v2h2V9h-2zm0 4v6h2v-6h-2z"/>
        <path d="M3 10v10c0 2.76 2.24 5 5 5h8c2.76 0 5-2.24 5-5V10H3zm7 10H8v-2h2v2zm4 0h-2v-2h2v2zm4 0h-2v-2h2v2zm0-4H6v-2h12v2z"/>
      </svg>
    </div>
    <div class="absolute bottom-40 left-1/3 w-20 h-20 text-purple-300/20 animate-float">
      <svg fill="currentColor" viewBox="0 0 24 24" class="drop-shadow-xl">
        <path d="M19 9.3V4h-3v2.6L12 3L2 12h3v8h5v-6h4v6h5v-8h3l-3-2.7zM10 10c0-1.1.9-2 2-2s2 .9 2 2h-4z"/>
      </svg>
    </div>
    <div class="absolute top-1/2 left-12 w-14 h-14 text-blue-200/25 animate-float-delayed">
      <svg fill="currentColor" viewBox="0 0 24 24" class="drop-shadow-md">
        <path d="M7 13c1.66 0 3-1.34 3-3S8.66 7 7 7s-3 1.34-3 3 1.34 3 3 3zm12-6h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06L14.17 0 7.59 6.59C7.22 6.95 7 7.45 7 8v10c0 1.1.9 2 2 2h9c.83 0 1.54-.5 1.84-1.22l3.02-7.05c.09-.23.14-.47.14-.73v-2c0-1.1-.9-2-2-2z"/>
      </svg>
    </div>

    <!-- Animated Circles -->
    <div class="circle-animation absolute top-1/4 left-1/4 w-64 h-64 rounded-full bg-blue-400/10 animate-pulse-slow"></div>
    <div class="circle-animation absolute bottom-1/4 right-1/4 w-96 h-96 rounded-full bg-purple-400/10 animate-pulse-slower"></div>
  </div>
</template>

<style scoped>
.animated-background {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(5deg);
  }
}

@keyframes float-delayed {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-30px) rotate(-5deg);
  }
}

@keyframes float-slow {
  0%, 100% {
    transform: translateY(0px) scale(1);
  }
  50% {
    transform: translateY(-15px) scale(1.05);
  }
}

@keyframes pulse-slow {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.1);
  }
}

@keyframes pulse-slower {
  0%, 100% {
    opacity: 0.2;
    transform: scale(1);
  }
  50% {
    opacity: 0.4;
    transform: scale(1.05);
  }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

.animate-float-delayed {
  animation: float-delayed 7s ease-in-out infinite;
  animation-delay: 1s;
}

.animate-float-slow {
  animation: float-slow 8s ease-in-out infinite;
  animation-delay: 2s;
}

.animate-pulse-slow {
  animation: pulse-slow 4s ease-in-out infinite;
}

.animate-pulse-slower {
  animation: pulse-slower 6s ease-in-out infinite;
}
</style>
