import "./common.css"
import "./section3.css"
import { useState } from "react";
import { Tabs, TabList, Tab, TabPanel } from "react-tabs";
import "react-tabs/style/react-tabs.css";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from "recharts";

const recommendations = {
  musk: {
    remedy: "Neem oil spray is an effective and eco-friendly alternative for controlling musk pests.",
    dosage: "Mix 5ml of neem oil with 1 liter of water and spray on affected plants every 7 days.",
  },
  // Add more pesticides here...
};

const detectionHistory = [
  { date: "Jan", cases: 5 },
  { date: "Feb", cases: 9 },
  { date: "Mar", cases: 12 },
  { date: "Apr", cases: 7 },
  { date: "May", cases: 15 },
];

const seasonalTrends = [
  { season: "Spring", cases: 10 },
  { season: "Summer", cases: 20 },
  { season: "Autumn", cases: 8 },
  { season: "Winter", cases: 5 },
];

const pesticideDistribution = [
  { name: "Musk", value: 45 },
  { name: "Alpha", value: 25 },
  { name: "Beta", value: 30 },
];

const COLORS = ["#0088FE", "#00C49F", "#FFBB28"];

const Recommendations = ({ detectedPesticide }) => {
  const pesticideInfo = recommendations[detectedPesticide] || {
    remedy: "No specific remedy found.",
    dosage: "No dosage guidelines available.",
  };

  const [tabIndex, setTabIndex] = useState(0);

  return (
    <div className="rec-container">
      {/* 🔹 Heading */}
      <h4 className="inputheading">🛠️ Recommendations & Solutions</h4>

      {/* 🔹 Remedies */}
      <div className="remedy-container">
        <strong>Suggested Remedy:</strong>
        <p>{pesticideInfo.remedy}</p>
      </div>

      {/* 🔹 Dosage */}
      <div className="remedy-container">
        <strong>Dosage & Application:</strong>
        <p>{pesticideInfo.dosage}</p>
      </div>

      {/* 🔹 Smart Alerts */}
     

      {/* 🔹 Graphs (Tabbed) */}
      <Tabs selectedIndex={tabIndex} onSelect={(index) => setTabIndex(index)} className="Tabs">
        <TabList className="TabList">
          <Tab className="TabListitem">📊 Detection Trends</Tab>
          <Tab className="TabListitem">🌱 Seasonal Trends</Tab>
          <Tab className="TabListitem">🧪 Pesticide Distribution</Tab>
        </TabList>

        {/* 🔹 Detection Trends Graph */}
        <TabPanel>
          <h3 className="text-lg font-semibold">📊 Detection History & Trends</h3>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={detectionHistory}>
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <CartesianGrid strokeDasharray="3 3" />
              <Line type="monotone" dataKey="cases" stroke="#8884d8" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </TabPanel>

        {/* 🔹 Seasonal Trends Graph */}
        <TabPanel>
          <h3 className="text-lg font-semibold">🌱 Seasonal Trends</h3>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={seasonalTrends}>
              <XAxis dataKey="season" />
              <YAxis />
              <Tooltip />
              <CartesianGrid strokeDasharray="3 3" />
              <Bar dataKey="cases" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        </TabPanel>

        {/* 🔹 Pesticide Distribution Graph */}
        <TabPanel>
          <h3 className="text-lg font-semibold">🧪 Pesticide Distribution</h3>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={pesticideDistribution} cx="50%" cy="50%" outerRadius={100} label>
                {pesticideDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </TabPanel>
      </Tabs>
    </div>
  );
};

export default Recommendations;
