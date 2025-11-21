import { motion } from 'framer-motion';

// Employee Profile Card
export const EmployeeCard = ({ data }: { data: any }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white/80 backdrop-blur-lg rounded-2xl p-5 border border-gray-200 shadow-soft max-w-md"
    >
      <div className="flex items-start gap-4">
        <div className="w-16 h-16 bg-gradient-to-br from-accent to-purple-600 rounded-xl flex items-center justify-center text-white text-2xl font-bold">
          {data.initials || 'JD'}
        </div>
        <div className="flex-grow">
          <h4 className="text-lg font-bold text-primary">{data.name || 'John Doe'}</h4>
          <p className="text-sm text-gray-600">{data.role || 'Senior Engineer'}</p>
          <div className="flex items-center gap-2 mt-2">
            <span className={`px-2 py-1 text-xs rounded-full ${data.status === 'Active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'}`}>
              {data.status || 'Active'}
            </span>
            <span className="text-xs text-gray-500">Joined {data.startDate || 'Jan 2020'}</span>
          </div>
        </div>
      </div>
      <div className="mt-4 pt-4 border-t border-gray-200 flex gap-2">
        <button className="flex-1 px-3 py-2 bg-accent text-white rounded-lg text-sm font-medium hover:bg-blue-600 transition-colors">
          📧 Email
        </button>
        <button className="flex-1 px-3 py-2 bg-neutral text-primary rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors">
          📞 Call
        </button>
      </div>
    </motion.div>
  );
};

// Policy Summary Card
export const PolicyCard = ({ data }: { data: any }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white/80 backdrop-blur-lg rounded-2xl p-5 border border-gray-200 shadow-soft"
    >
      <div className="flex items-start justify-between mb-3">
        <div>
          <h4 className="text-lg font-bold text-primary">{data.title || 'Leave Policy'}</h4>
          <p className="text-xs text-gray-500">Updated {data.updated || 'Mar 2024'}</p>
        </div>
        <span className="px-3 py-1 bg-blue-100 text-blue-700 text-xs font-medium rounded-full">
          Policy
        </span>
      </div>
      <p className="text-sm text-gray-700 mb-4 leading-relaxed">
        {data.summary || 'Employees are entitled to 20 days of paid leave annually, with the ability to carry over up to 5 days to the next year.'}
      </p>
      <details className="text-sm">
        <summary className="cursor-pointer text-accent font-medium">View full policy</summary>
        <div className="mt-3 p-3 bg-neutral rounded-lg text-gray-700 leading-relaxed">
          {data.fullText || 'Full policy details would appear here...'}
        </div>
      </details>
      <div className="mt-4 pt-3 border-t border-gray-200 flex items-center gap-2 text-xs text-gray-500">
        <span>📄</span>
        <span>Source: HR Policy Handbook v3.2</span>
      </div>
    </motion.div>
  );
};

// Analytics Card
export const AnalyticsCard = ({ data }: { data: any }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white/80 backdrop-blur-lg rounded-2xl p-5 border border-gray-200 shadow-soft"
    >
      <h4 className="text-lg font-bold text-primary mb-4">{data.title || 'HR Analytics'}</h4>
      <div className="grid grid-cols-3 gap-4 mb-4">
        <div className="text-center p-3 bg-blue-50 rounded-xl">
          <div className="text-2xl font-bold text-accent">{data.metric1 || '142'}</div>
          <div className="text-xs text-gray-600 mt-1">Total Employees</div>
        </div>
        <div className="text-center p-3 bg-green-50 rounded-xl">
          <div className="text-2xl font-bold text-green-600">{data.metric2 || '12'}</div>
          <div className="text-xs text-gray-600 mt-1">On Leave</div>
        </div>
        <div className="text-center p-3 bg-orange-50 rounded-xl">
          <div className="text-2xl font-bold text-orange-600">{data.metric3 || '8%'}</div>
          <div className="text-xs text-gray-600 mt-1">Turnover Rate</div>
        </div>
      </div>
      <div className="h-32 bg-neutral rounded-xl flex items-center justify-center text-gray-400">
        📊 Chart visualization would render here
      </div>
    </motion.div>
  );
};

// Task/Ticket Card
export const TaskCard = ({ data }: { data: any }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white/80 backdrop-blur-lg rounded-2xl p-5 border border-gray-200 shadow-soft"
    >
      <div className="flex items-start gap-3 mb-3">
        <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center text-accent font-bold">
          {data.icon || '📋'}
        </div>
        <div className="flex-grow">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-mono text-gray-500">{data.id || 'JIRA-1234'}</span>
            <span className={`px-2 py-0.5 text-xs rounded ${data.priority === 'High' ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'}`}>
              {data.priority || 'Medium'}
            </span>
          </div>
          <h4 className="font-semibold text-primary">{data.title || 'Update employee handbook'}</h4>
        </div>
      </div>
      <p className="text-sm text-gray-600 mb-3">{data.description || 'Review and update the employee handbook to reflect new remote work policies.'}</p>
      <div className="flex items-center justify-between text-xs">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full" />
          <span className="text-gray-600">{data.assignee || 'Sarah Chen'}</span>
        </div>
        <span className="text-gray-500">{data.dueDate || 'Due in 3 days'}</span>
      </div>
    </motion.div>
  );
};

// SQL Query Card
export const SQLCard = ({ data }: { data: any }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white/80 backdrop-blur-lg rounded-2xl p-5 border border-gray-200 shadow-soft"
    >
      <div className="flex items-center justify-between mb-3">
        <h4 className="text-lg font-bold text-primary">SQL Query</h4>
        <span className="px-2 py-1 bg-purple-100 text-purple-700 text-xs font-medium rounded">
          PostgreSQL
        </span>
      </div>
      <div className="bg-[#1e1e1e] rounded-xl p-4 font-mono text-sm text-white overflow-x-auto mb-3">
        <pre className="whitespace-pre-wrap">
          <code>
            {data.query || `SELECT name, department, hire_date
FROM employees
WHERE hire_date > '2020-01-01'
AND department = 'Engineering'
ORDER BY hire_date DESC;`}
          </code>
        </pre>
      </div>
      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        className="px-4 py-2 bg-accent text-white rounded-lg text-sm font-medium hover:bg-blue-600 transition-colors"
      >
        ▶ Run Query
      </motion.button>
    </motion.div>
  );
};
