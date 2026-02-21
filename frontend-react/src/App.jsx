import React from "react";
import { useSSE } from "./hooks/useSSE";
import KPICards from "./components/KPICards";
import AlertFeed from "./components/AlertFeed";
import TransactionList from "./components/TransactionList";
import NetworkGraph from "./components/NetworkGraph";
import PreTxChecker from "./components/PreTxChecker";
import { FraudRings, MuleAccounts } from "./components/FraudIntelligence";
import "./App.css";

export default function App() {
  const {
    latestTx,
    history,
    graph,
    fraudRings,
    muleAccounts,
    alertCount,
    txCount,
  } = useSSE();

  return (
    <div className="app">
      {/* ── NAVBAR ────────────────────────────────────────────── */}
      <nav className="navbar">
        <div className="logo">UPI Shield</div>
        <div className="nav-links">
          <span>Dashboard</span>
          <span>Analytics</span>
          <span>Alerts</span>
          <span>About</span>
        </div>
      </nav>

      {/* ── HERO ─────────────────────────────────────────────── */}
      <div className="hero">
        <h1>Detect UPI Fraud in Real Time</h1>
        <p>AI-powered transaction monitoring and fraud intelligence platform</p>
        <div className="hero-search">
          <input placeholder="Search transaction / user ID" />
          <button>Analyze</button>
        </div>
      </div>

      {/* ── KPI CARDS ─────────────────────────────────────────── */}
      <KPICards latestTx={latestTx} txCount={txCount} alertCount={alertCount} />

      {/* ── MAIN DASHBOARD ────────────────────────────────────── */}
      <div className="dashboard">
        {/* Network Graph */}
        <NetworkGraph graphData={graph} latestTx={latestTx} />

        {/* Right panel */}
        <div className="side">
          <AlertFeed latestTx={latestTx} alertCount={alertCount} />
          <TransactionList history={history} />
        </div>
      </div>

      {/* ── FRAUD INTELLIGENCE ────────────────────────────────── */}
      <div className="intelligence-section">
        <h2 className="section-title">🔍 Fraud Intelligence</h2>
        <div className="intelligence-grid">
          <FraudRings rings={fraudRings} />
          <MuleAccounts mules={muleAccounts} />
          <PreTxChecker />
        </div>
      </div>

      {/* ── ABOUT ─────────────────────────────────────────────── */}
      <div className="about">
        <h2>About UPI Shield</h2>
        <p>
          UPI Shield is a real-time fraud intelligence platform designed to
          detect suspicious digital payment transactions using AI and network
          analytics. It uses a <strong>Random Forest Classifier</strong>,
          rule-based risk analysis, graph-based <strong>fraud ring and mule account detection</strong>, and
          a <strong>pre-transaction blocking API</strong> to stop fraud before completion.
        </p>
      </div>

      {/* ── FOOTER ────────────────────────────────────────────── */}
      <footer className="footer">
        <div className="footer-col">
          <h4>Company</h4>
          <a href="#about">About Us</a>
          <a href="#careers">Careers</a>
          <a href="#blog">Blog</a>
        </div>
        <div className="footer-col">
          <h4>Services</h4>
          <a href="#monitor">Fraud Monitoring</a>
          <a href="#risk">Risk Analytics</a>
          <a href="#intel">Transaction Intelligence</a>
        </div>
        <div className="footer-col">
          <h4>Team</h4>
          <p>Developed by</p>
          <span className="team-name">Team Code Blooded</span>
        </div>
      </footer>
    </div>
  );
}
