import React, { useState, useEffect } from 'react';
import { CheckCircle, Clock } from 'lucide-react';
import { api } from '../utils/api';
import './LessonCard.css';

export default function LessonCard({ lesson, isSelected, onSelect, token }) {
  const [attempts, setAttempts] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const loadAttempts = async () => {
      setLoading(true);
      try {
        const res = await api(token).get(`/quiz/attempts/${lesson.slug}`);
        setAttempts(res.data?.attempts || []);
      } catch (err) {
        // Endpoint not yet implemented - show no attempts
        setAttempts([]);
      } finally {
        setLoading(false);
      }
    };

    if (token) {
      loadAttempts();
    }
  }, [lesson.slug, token]);

  const getProgressPercentage = () => {
    if (!attempts || attempts.length === 0) return 0;
    const avgScore = attempts.reduce((sum, a) => sum + a.quiz_score, 0) / attempts.length;
    return Math.round(avgScore);
  };

  const hasCompleted = attempts && attempts.length > 0;
  const bestScore = attempts && attempts.length > 0 
    ? Math.max(...attempts.map(a => a.quiz_score))
    : 0;

  return (
    <div 
      className={`lesson-card ${isSelected ? 'selected' : ''} ${hasCompleted ? 'completed' : ''}`}
      onClick={onSelect}
    >
      <div className="lesson-card-header">
        <h3 className="lesson-card-title">{lesson.title}</h3>
        {hasCompleted && <CheckCircle size={20} className="completed-icon" />}
      </div>

      <p className="lesson-card-description">{lesson.description}</p>

      <div className="lesson-card-stats">
        {!loading && attempts ? (
          <>
            <div className="stat-item">
              <span className="stat-label">Attempts</span>
              <span className="stat-value">{attempts.length}</span>
            </div>
            {hasCompleted && (
              <div className="stat-item">
                <span className="stat-label">Best Score</span>
                <span className="stat-value">{bestScore}%</span>
              </div>
            )}
          </>
        ) : (
          <div className="stat-item">
            <Clock size={14} />
            <span className="stat-label">Loading...</span>
          </div>
        )}
      </div>

      {hasCompleted && (
        <div className="progress-bar">
          <div 
            className="progress-fill"
            style={{ width: `${getProgressPercentage()}%` }}
          ></div>
        </div>
      )}

      <button
        className="btn-start-lesson"
        onClick={(e) => {
          e.stopPropagation();
          console.log('LessonCard start clicked for', lesson.slug);
          if (onSelect) onSelect();
        }}
      >
        {hasCompleted ? 'Continue' : 'Start'} Lesson →
      </button>
    </div>
  );
}
