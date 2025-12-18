import React, { useEffect, useState } from 'react';
import LessonCard from '../components/LessonCard';
import LessonDetail from '../components/LessonDetail';
import QuizInterface from '../components/QuizInterface';
import ProgressPanel from '../components/ProgressPanel';
import { api } from '../utils/api';
import './Dashboard.css';
import { Book, BarChart3, Download, LogOut } from 'lucide-react';

export default function Dashboard({ token, onLogout }) {
  const [lessons, setLessons] = useState([]);
  const [view, setView] = useState('lessons'); // 'lessons', 'lesson-detail', 'quiz', 'progress'
  const [selectedLessonSlug, setSelectedLessonSlug] = useState(null);
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState(null);
  const [exporting, setExporting] = useState(false);

  // Fetch lessons
  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      setErrorMsg(null);
      try {
        const lessonsRes = await api(token).get('/lessons');
        const serverLessons = lessonsRes.data || [];
        setLessons(serverLessons);
      } catch (err) {
        console.error('Failed to load lessons:', err);
        setErrorMsg('Failed to load lessons. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [token]);

  const handleExportProgress = async () => {
    setExporting(true);
    try {
      const res = await api(token).get('/progress/export?format=csv');
      const csvData = res.data?.data || res.data;
      const blob = new Blob([csvData], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `progress_${new Date().toISOString().split('T')[0]}.csv`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error('Export failed:', e);
      alert('Failed to export progress');
    } finally {
      setExporting(false);
    }
  };

  const handleStartQuiz = (lessonSlug) => {
    console.log('handleStartQuiz called for', lessonSlug);
    setSelectedLessonSlug(lessonSlug);
    setView('quiz');
  };

  const handleBack = () => {
    setView('lessons');
    setSelectedLessonSlug(null);
  };

  const handleQuizComplete = () => {
    setView('lessons');
    setSelectedLessonSlug(null);
  };

  if (loading) {
    return (
      <div className="dashboard-wrapper">
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <div className="spinner"></div>
          <p style={{ marginTop: '1rem', color: '#666' }}>Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (errorMsg) {
    return (
      <div className="dashboard-wrapper">
        <div className="error-banner">{errorMsg}</div>
      </div>
    );
  }

  return (
    <div className="dashboard-wrapper">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <h1 className="app-title">Language Tutor</h1>
          <p className="app-subtitle">Master English with interactive lessons</p>
        </div>
        <div className="header-actions">
          <button 
            className="btn-icon" 
            onClick={handleExportProgress}
            disabled={exporting}
            title="Export your progress as CSV"
          >
            <Download size={18} />
            {exporting ? 'Exporting...' : 'Export'}
          </button>
          <button 
            className="btn-icon danger" 
            onClick={onLogout}
            title="Logout"
          >
            <LogOut size={18} />
            Logout
          </button>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="dashboard-nav">
        <button
          className={`nav-tab ${view === 'lessons' ? 'active' : ''}`}
          onClick={() => setView('lessons')}
        >
          <Book size={18} />
          Lessons
        </button>
        <button
          className={`nav-tab ${view === 'progress' ? 'active' : ''}`}
          onClick={() => setView('progress')}
        >
          <BarChart3 size={18} />
          Progress
        </button>
      </div>

      {/* Content Area */}
      <div className="dashboard-content">
        {view === 'lessons' && (
          <div className="lessons-view">
            <h2 className="section-title">Available Lessons</h2>
            <div className="cards-grid">
              {lessons.map((lesson) => (
                <LessonCard
                  key={lesson._id || lesson.slug}
                  lesson={lesson}
                  onSelect={() => {
                    setSelectedLessonSlug(lesson.slug);
                    setView('lesson-detail');
                  }}
                  token={token}
                />
              ))}
            </div>
          </div>
        )}

        {view === 'lesson-detail' && selectedLessonSlug && (
          <LessonDetail
            lessonSlug={selectedLessonSlug}
            token={token}
            onBack={handleBack}
            onStartQuiz={handleStartQuiz}
          />
        )}

        {view === 'quiz' && selectedLessonSlug && (
          <QuizInterface
            lessonSlug={selectedLessonSlug}
            token={token}
            onBack={handleBack}
            onComplete={handleQuizComplete}
          />
        )}

        {view === 'progress' && (
          <ProgressPanel progress={progress} token={token} />
        )}
      </div>
    </div>
  );
}
