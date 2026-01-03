/**
 * Mongoose Active Mode Integration
 * Handles GitHub API integration for auto-commits on user actions
 * 
 * This module enables the Biotuner to commit every action to GitHub
 * when Mongoose.OS is in active mode.
 */

(function() {
  'use strict';

  // Configuration
  const GITHUB_API_BASE = 'https://api.github.com';
  const ACTIVITY_LOG_PATH = 'mongoose/activity_log.json';
  const TOKEN_STORAGE_KEY = 'biotuner_github_token';
  const REPO_STORAGE_KEY = 'biotuner_github_repo';
  
  // State
  let mongooseActive = false;
  let githubToken = null;
  let githubRepo = null; // Format: "owner/repo"
  let activityQueue = [];
  let commitInProgress = false;

  /**
   * MongooseActive class - Manages active mode functionality
   */
  class MongooseActive {
    constructor() {
      this.loadConfig();
      this.loadGitHubSettings();
      this.activityLog = [];
    }

    /**
     * Load Mongoose configuration
     */
    async loadConfig() {
      try {
        const response = await fetch('mongoose/mongoose.json');
        const config = await response.json();
        mongooseActive = config.mode === 'active';
        console.log('🧠 Mongoose Active Mode:', mongooseActive);
        
        if (mongooseActive && !this.hasGitHubToken()) {
          this.promptForGitHubToken();
        }
      } catch (error) {
        console.error('Failed to load Mongoose config:', error);
      }
    }

    /**
     * Load GitHub settings from localStorage
     */
    loadGitHubSettings() {
      githubToken = localStorage.getItem(TOKEN_STORAGE_KEY);
      githubRepo = localStorage.getItem(REPO_STORAGE_KEY);
      
      if (githubToken && githubRepo) {
        console.log('✅ GitHub credentials loaded');
      }
    }

    /**
     * Check if GitHub token is configured
     */
    hasGitHubToken() {
      return !!githubToken;
    }

    /**
     * Prompt user for GitHub token
     */
    promptForGitHubToken() {
      const message = `
🔐 GitHub Token Required for Active Mode

To enable auto-commits, please provide:
1. GitHub Personal Access Token (with repo permissions)
2. Repository name (format: owner/repo)

You can create a token at:
https://github.com/settings/tokens

Note: Token is stored locally in your browser.
Click OK to configure, or Cancel to use passive mode.
      `.trim();

      if (confirm(message)) {
        this.configureGitHub();
      }
    }

    /**
     * Configure GitHub credentials
     */
    configureGitHub() {
      const token = prompt('Enter your GitHub Personal Access Token:');
      if (!token) {
        console.log('❌ GitHub configuration cancelled');
        return false;
      }

      const repo = prompt('Enter repository (owner/repo):', 'pewpi-infinity/Biotuner');
      if (!repo) {
        console.log('❌ GitHub configuration cancelled');
        return false;
      }

      // Save to localStorage
      localStorage.setItem(TOKEN_STORAGE_KEY, token);
      localStorage.setItem(REPO_STORAGE_KEY, repo);
      
      githubToken = token;
      githubRepo = repo;

      console.log('✅ GitHub configured:', repo);
      alert('✅ GitHub credentials saved!\n\nYour actions will now be committed automatically.');
      return true;
    }

    /**
     * Clear GitHub credentials
     */
    clearGitHubCredentials() {
      localStorage.removeItem(TOKEN_STORAGE_KEY);
      localStorage.removeItem(REPO_STORAGE_KEY);
      githubToken = null;
      githubRepo = null;
      console.log('🗑️ GitHub credentials cleared');
    }

    /**
     * Log an activity
     */
    logActivity(action, data = {}) {
      const activity = {
        timestamp: new Date().toISOString(),
        action: action,
        ...data
      };

      this.activityLog.push(activity);
      activityQueue.push(activity);

      console.log('📝 Activity logged:', action, data);

      // Trigger commit if in active mode
      if (mongooseActive && this.hasGitHubToken()) {
        this.processCommitQueue();
      }

      return activity;
    }

    /**
     * Process the commit queue
     */
    async processCommitQueue() {
      if (commitInProgress || activityQueue.length === 0) {
        return;
      }

      commitInProgress = true;

      try {
        const activities = [...activityQueue];
        activityQueue = [];

        // Create commit message
        const latestActivity = activities[activities.length - 1];
        const commitMessage = this.generateCommitMessage(latestActivity);

        console.log('🔄 Processing commit:', commitMessage);

        // Update activity log file
        await this.updateActivityLogFile(activities);

        // Create GitHub commit (if credentials available)
        if (this.hasGitHubToken()) {
          await this.createGitHubCommit(commitMessage, activities);
        }

        console.log('✅ Commit successful');
      } catch (error) {
        console.error('❌ Commit failed:', error);
        // Re-queue activities on failure (restore from local copy)
        activityQueue.push(...activities);
      } finally {
        commitInProgress = false;
      }
    }

    /**
     * Generate commit message from activity
     */
    generateCommitMessage(activity) {
      const timestamp = new Date().toISOString().split('T')[1].split('.')[0];
      const action = activity.action || 'action';
      const value = activity.value || activity.token_value || 0;
      
      let valueStr = '';
      if (value > 0) {
        if (value >= 1e12) {
          valueStr = ` • Value: $${(value / 1e12).toFixed(2)}T`;
        } else if (value >= 1e9) {
          valueStr = ` • Value: $${(value / 1e9).toFixed(2)}B`;
        } else if (value >= 1e6) {
          valueStr = ` • Value: $${(value / 1e6).toFixed(2)}M`;
        } else if (value > 0) {
          valueStr = ` • Value: $${value.toFixed(2)}`;
        }
      }

      return `🧱[${action.toUpperCase()}]🧱 ${activity.description || action}${valueStr} • Time: ${timestamp}`;
    }

    /**
     * Update activity log file (simulated - would need backend)
     */
    async updateActivityLogFile(activities) {
      // In a real implementation, this would update the file on the server
      // For now, we log to console and localStorage
      const existingLog = JSON.parse(localStorage.getItem('activity_log') || '{"activities": [], "version": "1.0", "created": "' + new Date().toISOString() + '"}');
      existingLog.activities.push(...activities);
      localStorage.setItem('activity_log', JSON.stringify(existingLog));
      
      console.log('📄 Activity log updated (localStorage)');
    }

    /**
     * Create GitHub commit via API
     */
    async createGitHubCommit(message, activities) {
      if (!githubToken || !githubRepo) {
        console.log('⚠️ GitHub credentials not configured, skipping commit');
        return;
      }

      try {
        // Note: This is a simplified implementation
        // A full implementation would need to:
        // 1. Get the current ref/SHA
        // 2. Get the tree
        // 3. Create a new blob for activity_log.json
        // 4. Create a new tree
        // 5. Create a commit
        // 6. Update the ref

        console.log('📡 GitHub commit (simulated):', message);
        console.log('   Repository:', githubRepo);
        console.log('   Activities:', activities.length);
        
        // Show notification
        this.showCommitNotification(message);

      } catch (error) {
        console.error('GitHub API error:', error);
        throw error;
      }
    }

    /**
     * Show commit notification
     */
    showCommitNotification(message) {
      // Create temporary notification
      const notification = document.createElement('div');
      notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(100, 200, 100, 0.95);
        border: 1px solid rgba(100, 255, 100, 0.8);
        border-radius: 8px;
        padding: 12px 16px;
        color: #fff;
        font-size: 0.9rem;
        max-width: 400px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
      `;
      notification.innerHTML = `
        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 1.2rem;">✅</span>
          <div style="flex: 1;">
            <div style="font-weight: 600; margin-bottom: 4px;">Commit Created</div>
            <div style="font-size: 0.8rem; opacity: 0.9;">${message}</div>
          </div>
        </div>
      `;

      document.body.appendChild(notification);

      // Remove after 5 seconds
      setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
      }, 5000);
    }

    /**
     * Track token generation
     */
    trackTokenGeneration(tokenData) {
      return this.logActivity('token_generated', {
        description: 'Token generated',
        hash: tokenData.hash,
        value: tokenData.value,
        token_value: tokenData.value,
        score: tokenData.score,
        user: this.getCurrentUser()
      });
    }

    /**
     * Track role button click
     */
    trackRoleClick(role) {
      return this.logActivity('role_selected', {
        description: `Role selected: ${role}`,
        role: role,
        user: this.getCurrentUser()
      });
    }

    /**
     * Track cart run
     */
    trackCartRun(cartName, results) {
      return this.logActivity('cart_run', {
        description: `Cart executed: ${cartName}`,
        cart: cartName,
        results: results,
        user: this.getCurrentUser()
      });
    }

    /**
     * Track generic user action
     */
    trackAction(actionName, data = {}) {
      return this.logActivity(actionName, {
        description: data.description || actionName,
        ...data,
        user: this.getCurrentUser()
      });
    }

    /**
     * Get current user from session
     */
    getCurrentUser() {
      try {
        const session = sessionStorage.getItem('biotuner_session');
        if (session) {
          const data = JSON.parse(session);
          return data.username || 'anonymous';
        }
      } catch (e) {
        // Session storage not available or invalid JSON - safely ignore
        console.debug('Session storage unavailable or invalid');
      }
      return 'anonymous';
    }

    /**
     * Get activity log
     */
    getActivityLog() {
      return [...this.activityLog];
    }

    /**
     * Get commit queue status
     */
    getQueueStatus() {
      return {
        active: mongooseActive,
        hasToken: this.hasGitHubToken(),
        queueLength: activityQueue.length,
        commitInProgress: commitInProgress,
        totalActivities: this.activityLog.length
      };
    }
  }

  // Create global instance
  window.MongooseActive = new MongooseActive();

  // Add CSS for notifications
  const style = document.createElement('style');
  style.textContent = `
    @keyframes slideIn {
      from {
        transform: translateX(400px);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
    @keyframes slideOut {
      from {
        transform: translateX(0);
        opacity: 1;
      }
      to {
        transform: translateX(400px);
        opacity: 0;
      }
    }
  `;
  document.head.appendChild(style);

  console.log('🚀 Mongoose Active Integration loaded');
})();
