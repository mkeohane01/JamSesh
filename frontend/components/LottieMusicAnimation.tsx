import React, { useEffect, useRef } from 'react';
import lottie from 'lottie-web';

const LottieAnimation = ({ animationData }: { animationData: any }) => {
  const animationContainer = useRef(null);
  const isClient = typeof window !== 'undefined';

  useEffect(() => {
    if (isClient && animationContainer.current) {
      const anim = lottie.loadAnimation({
        container: animationContainer.current,
        renderer: 'svg',
        loop: true,
        autoplay: true,
        animationData,
      });

      return () => anim.destroy();
    }
  }, [animationData, isClient]);

  if (!isClient) {
    return null; // Render nothing on the server
  }

  return <div ref={animationContainer} />;
};

export default LottieAnimation;
