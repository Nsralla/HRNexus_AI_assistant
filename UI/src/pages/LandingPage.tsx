import Hero from '../components/sections/Hero';
import BeforeAfter from '../components/sections/BeforeAfter';
import Features from '../components/sections/Features';
import DemoStrip from '../components/sections/DemoStrip';
import HowItWorks from '../components/sections/HowItWorks';
import Integrations from '../components/sections/Integrations';
import Testimonials from '../components/sections/Testimonials';
import FinalCTA from '../components/sections/FinalCTA';
import Footer from '../components/sections/Footer';

const LandingPage = () => {
  return (
    <div className="min-h-screen">
      <Hero />
      <BeforeAfter />
      <Features />
      <DemoStrip />
      <HowItWorks />
      <Integrations />
      <Testimonials />
      <FinalCTA />
      <Footer />
    </div>
  );
};

export default LandingPage;
