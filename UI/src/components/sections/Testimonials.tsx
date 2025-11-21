import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';

const Testimonials = () => {
  const testimonials = [
    {
      quote: "Finding HR answers went from minutes to seconds.",
      author: "Sarah Chen",
      role: "Operations Manager",
      company: "TechCorp Inc."
    },
    {
      quote: "Onboarding is literally 3x faster with the AI assistant.",
      author: "Michael Rodriguez",
      role: "HR Director",
      company: "InnovateLabs"
    },
    {
      quote: "Our team saves over 15 hours per week on HR queries.",
      author: "Emily Watson",
      role: "People Operations Lead",
      company: "GrowthStart"
    }
  ];

  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % testimonials.length);
    }, 5000);

    return () => clearInterval(timer);
  }, [testimonials.length]);

  const goToSlide = (index: number) => {
    setCurrentIndex(index);
  };

  return (
    <section className="py-24 bg-white overflow-hidden">
      <div className="container mx-auto px-6 lg:px-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-5xl font-extrabold text-primary mb-4">
            Loved by HR Teams
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            See what our customers are saying
          </p>
        </motion.div>

        <div className="relative max-w-4xl mx-auto">
          {/* Testimonial Cards */}
          <div className="relative h-64 md:h-56">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={index}
                initial={false}
                animate={{
                  opacity: index === currentIndex ? 1 : 0,
                  x: index === currentIndex ? 0 : index < currentIndex ? -100 : 100,
                  display: index === currentIndex ? 'block' : 'none'
                }}
                transition={{ duration: 0.5 }}
                className="absolute inset-0"
              >
                <div className="bg-gradient-to-br from-neutral to-white rounded-2xl p-10 shadow-soft h-full flex flex-col justify-between">
                  <div>
                    <div className="text-accent text-5xl mb-4">"</div>
                    <p className="text-2xl text-gray-700 leading-relaxed mb-6 font-medium">
                      {testimonial.quote}
                    </p>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="w-14 h-14 bg-gradient-to-br from-accent to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-xl">
                      {testimonial.author.split(' ').map(n => n[0]).join('')}
                    </div>
                    <div>
                      <p className="font-bold text-primary text-lg">{testimonial.author}</p>
                      <p className="text-gray-600">{testimonial.role}</p>
                      <p className="text-gray-500 text-sm">{testimonial.company}</p>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Dots Navigation */}
          <div className="flex justify-center gap-2 mt-8">
            {testimonials.map((_, index) => (
              <button
                key={index}
                onClick={() => goToSlide(index)}
                className={`w-3 h-3 rounded-full transition-all ${
                  index === currentIndex
                    ? 'bg-accent w-8'
                    : 'bg-gray-300 hover:bg-gray-400'
                }`}
                aria-label={`Go to testimonial ${index + 1}`}
              />
            ))}
          </div>
        </div>

        {/* Stats Bar */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="grid md:grid-cols-3 gap-8 mt-16 max-w-4xl mx-auto"
        >
          <div className="text-center">
            <div className="text-5xl font-extrabold text-accent mb-2">10x</div>
            <p className="text-gray-600">Faster Response Time</p>
          </div>
          <div className="text-center">
            <div className="text-5xl font-extrabold text-accent mb-2">95%</div>
            <p className="text-gray-600">Accuracy Rate</p>
          </div>
          <div className="text-center">
            <div className="text-5xl font-extrabold text-accent mb-2">24/7</div>
            <p className="text-gray-600">Always Available</p>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default Testimonials;
