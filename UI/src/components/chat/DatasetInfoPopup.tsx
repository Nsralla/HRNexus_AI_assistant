import { Database, ExternalLink, X } from 'lucide-react';
import { useState } from 'react';

const DatasetInfoPopup = () => {
  const [isVisible, setIsVisible] = useState(true);
  const [isMinimized, setIsMinimized] = useState(false);

  if (!isVisible) return null;

  return (
    <div
      className={`fixed bottom-6 right-6 z-50 transition-all duration-300 ${
        isMinimized ? 'w-16 h-16' : 'w-96'
      }`}
    >
      {isMinimized ? (
        // Minimized floating button
        <button
          onClick={() => setIsMinimized(false)}
          className="w-16 h-16 bg-gradient-to-br from-primary to-primary/80 rounded-full shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center group hover:scale-110"
          aria-label="Show dataset info"
        >
          <Database className="w-7 h-7 text-white group-hover:rotate-12 transition-transform" />
          <div className="absolute -top-1 -right-1 w-3 h-3 bg-blue-400 rounded-full animate-pulse" />
        </button>
      ) : (
        // Expanded card
        <div className="bg-white rounded-2xl shadow-2xl border border-gray-200 overflow-hidden animate-slideIn">
          {/* Header */}
          <div className="bg-gradient-to-r from-primary to-primary/90 p-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-white/20 rounded-lg backdrop-blur-sm">
                <Database className="w-5 h-5 text-white" />
              </div>
              <div>
                <h3 className="text-white font-semibold text-sm">Dataset Explorer</h3>
                <p className="text-white/80 text-xs">Behind the scenes</p>
              </div>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setIsMinimized(true)}
                className="p-1.5 hover:bg-white/20 rounded-lg transition-colors"
                aria-label="Minimize"
              >
                <div className="w-4 h-0.5 bg-white rounded" />
              </button>
              <button
                onClick={() => setIsVisible(false)}
                className="p-1.5 hover:bg-white/20 rounded-lg transition-colors"
                aria-label="Close"
              >
                <X className="w-4 h-4 text-white" />
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="p-5">
            <div className="mb-4">
              <p className="text-gray-700 text-sm leading-relaxed">
                <span className="font-semibold text-gray-900">New here?</span> Not sure what to ask?
              </p>
              <p className="text-gray-600 text-xs mt-2">
                Explore the complete dataset powering HR Nexus to discover what you can query!
              </p>
            </div>

            {/* Dataset highlights */}
            <div className="bg-gray-50 rounded-lg p-3 mb-4 border border-gray-100">
              <p className="text-xs font-semibold text-gray-700 mb-2">What's inside:</p>
              <div className="grid grid-cols-2 gap-2 text-xs text-gray-600">
                <div className="flex items-center gap-1.5">
                  <div className="w-1.5 h-1.5 bg-blue-500 rounded-full" />
                  <span>Employees & Teams</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <div className="w-1.5 h-1.5 bg-green-500 rounded-full" />
                  <span>Projects & Sprints</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <div className="w-1.5 h-1.5 bg-purple-500 rounded-full" />
                  <span>JIRA Tickets</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <div className="w-1.5 h-1.5 bg-orange-500 rounded-full" />
                  <span>Services & Deploys</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <div className="w-1.5 h-1.5 bg-pink-500 rounded-full" />
                  <span>Meetings & Docs</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <div className="w-1.5 h-1.5 bg-yellow-500 rounded-full" />
                  <span>Policies & Guides</span>
                </div>
              </div>
            </div>

            {/* CTA Button */}
            <a
              href="https://drive.google.com/drive/folders/1_6KZwEVSlU8FNIwHceHQFuFgPRjCts6H?usp=sharing"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-center gap-2 w-full bg-gradient-to-r from-primary to-primary/90 hover:from-primary/90 hover:to-primary text-white py-2.5 px-4 rounded-lg transition-all duration-300 hover:shadow-lg group"
            >
              <span className="text-sm font-medium">Explore Full Dataset</span>
              <ExternalLink className="w-4 h-4 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
            </a>

            {/* Footer hint */}
            <p className="text-center text-xs text-gray-400 mt-3">
              💡 Tip: Check the guide cards for quick queries
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default DatasetInfoPopup;
