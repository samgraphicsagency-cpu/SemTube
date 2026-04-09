<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SemTube AI • YouTube Empire Builder</title>
    <link href="https://cdn.jsdelivr.net/npm/@fontsource/inter@5.0.16/index.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/@fontsource/poppins@5.0.14/index.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/@google/generative-ai@0.21.0/dist/index.min.js"></script>
    <style>
        :root {
            /* Primary Colors */
            --primary-start: #7c3aed;
            --primary-end: #3b82f6;
            --primary-glow: rgba(124, 58, 237, 0.4);
            
            /* Secondary */
            --secondary-start: #06b6d4;
            --secondary-end: #8b5cf6;
            
            /* Background */
            --bg-base: #0a0a0f;
            --bg-surface: rgba(20, 20, 35, 0.7);
            --bg-surface-hover: rgba(30, 30, 50, 0.9);
            --bg-card: rgba(25, 25, 45, 0.6);
            --bg-card-border: rgba(124, 58, 237, 0.2);
            
            /* Text */
            --text-primary: #ffffff;
            --text-secondary: #a1a1aa;
            --text-muted: #71717a;
            --text-accent: #c4b5fd;
            
            /* Status */
            --success: #10b981;
            --success-glow: rgba(16, 185, 129, 0.3);
            --warning: #f59e0b;
            --warning-glow: rgba(245, 158, 11, 0.3);
            --error: #ef4444;
            --error-glow: rgba(239, 68, 68, 0.3);
            --info: #3b82f6;
            --info-glow: rgba(59, 130, 246, 0.3);
            
            /* Borders & Shadows */
            --border-subtle: rgba(255, 255, 255, 0.08);
            --border-focus: rgba(124, 58, 237, 0.6);
            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
            --shadow-md: 0 4px 20px rgba(0, 0, 0, 0.4);
            --shadow-lg: 0 8px 40px rgba(0, 0, 0, 0.5);
            --shadow-glow: 0 0 30px var(--primary-glow);
            
            /* Spacing */
            --radius-sm: 8px;
            --radius-md: 16px;
            --radius-lg: 24px;
            --radius-xl: 32px;
            --radius-full: 9999px;
            
            /* Transitions */
            --transition-fast: 150ms ease;
            --transition-normal: 300ms ease;
            --transition-slow: 500ms ease;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: 
                radial-gradient(ellipse at top, rgba(124, 58, 237, 0.15) 0%, transparent 50%),
                radial-gradient(ellipse at bottom right, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
                var(--bg-base);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.6;
            overflow-x: hidden;
        }

        /* Animated Background */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 80%, rgba(124, 58, 237, 0.1) 0%, transparent 40%),
                radial-gradient(circle at 80% 20%, rgba(59, 130, 246, 0.1) 0%, transparent 40%);
            pointer-events: none;
            z-index: -1;
            animation: bgPulse 8s ease-in-out infinite;
        }

        @keyframes bgPulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        /* Floating Particles */
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
            overflow: hidden;
        }

        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: var(--primary-start);
            border-radius: 50%;
            opacity: 0.3;
            animation: float 15s infinite linear;
        }

        @keyframes float {
            0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
            10% { opacity: 0.3; }
            90% { opacity: 0.3; }
            100% { transform: translateY(-100px) rotate(720deg); opacity: 0; }
        }

        /* Layout */
        .app-wrapper {
            display: flex;
            min-height: 100vh;
        }

        /* Sidebar */
        .sidebar {
            width: 320px;
            background: var(--bg-surface);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-right: 1px solid var(--border-subtle);
            padding: 28px 24px;
            position: fixed;
            height: 100vh;
            overflow-y: auto;
            z-index: 100;
            transition: transform var(--transition-normal);
            display: flex;
            flex-direction: column;
        }

        .sidebar::-webkit-scrollbar {
            width: 4px;
        }
        .sidebar::-webkit-scrollbar-track {
            background: transparent;
        }
        .sidebar::-webkit-scrollbar-thumb {
            background: var(--border-subtle);
            border-radius: 4px;
        }

        .sidebar-header {
            text-align: center;
            padding: 12px 0 28px;
            border-bottom: 1px solid var(--border-subtle);
            margin-bottom: 24px;
        }

        .logo {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            margin-bottom: 8px;
        }

        .logo-icon {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, var(--primary-start), var(--primary-end));
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            box-shadow: var(--shadow-glow);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { box-shadow: var(--shadow-glow); }
            50% { box-shadow: 0 0 50px var(--primary-glow); }
        }

        .logo-text {
            font-family: 'Poppins', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary-start), var(--secondary-end));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .logo-tagline {
            font-size: 0.75rem;
            color: var(--text-muted);
            letter-spacing: 2px;
            text-transform: uppercase;
            font-weight: 500;
        }

        .sidebar-section {
            margin-bottom: 28px;
        }

        .sidebar-section-title {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-accent);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .sidebar-section-title::before {
            content: '';
            width: 3px;
            height: 14px;
            background: linear-gradient(180deg, var(--primary-start), var(--primary-end));
            border-radius: 2px;
        }

        /* API Input */
        .api-card {
            background: var(--bg-card);
            border: 1px solid var(--bg-card-border);
            border-radius: var(--radius-md);
            padding: 16px;
            margin-bottom: 12px;
        }

        .api-input {
            width: 100%;
            padding: 12px 16px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-sm);
            color: var(--text-primary);
            font-size: 0.9rem;
            transition: all var(--transition-fast);
            font-family: inherit;
        }

        .api-input:focus {
            outline: none;
            border-color: var(--border-focus);
            box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.2);
            background: rgba(255, 255, 255, 0.08);
        }

        .api-input::placeholder {
            color: var(--text-muted);
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            border-radius: var(--radius-full);
            font-size: 0.8rem;
            font-weight: 500;
            margin-top: 10px;
            transition: all var(--transition-fast);
        }

        .status-pill.inactive {
            background: rgba(245, 158, 11, 0.15);
            color: var(--warning);
            border: 1px solid rgba(245, 158, 11, 0.3);
        }

        .status-pill.active {
            background: rgba(16, 185, 129, 0.15);
            color: var(--success);
            border: 1px solid rgba(16, 185, 129, 0.3);
            animation: statusGlow 2s infinite;
        }

        @keyframes statusGlow {
            0%, 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
            50% { box-shadow: 0 0 0 8px rgba(16, 185, 129, 0.1); }
        }

        .api-hint {
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 8px;
            line-height: 1.5;
        }

        .api-hint a {
            color: var(--primary-start);
            text-decoration: none;
            transition: color var(--transition-fast);
        }

        .api-hint a:hover {
            color: var(--primary-end);
            text-decoration: underline;
        }

        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }

        .stat-card-mini {
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.2), rgba(59, 130, 246, 0.15));
            border: 1px solid var(--bg-card-border);
            border-radius: var(--radius-md);
            padding: 18px 14px;
            text-align: center;
            transition: all var(--transition-fast);
        }

        .stat-card-mini:hover {
            transform: translateY(-2px);
            border-color: var(--primary-start);
        }

        .stat-value {
            font-size: 1.6rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary-start), var(--secondary-end));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .stat-label {
            font-size: 0.75rem;
            color: var(--text-secondary);
            margin-top: 4px;
            font-weight: 500;
        }

        /* Quick Start */
        .quick-start-list {
            list-style: none;
            font-size: 0.9rem;
            color: var(--text-secondary);
        }

        .quick-start-list li {
            padding: 8px 0;
            padding-left: 24px;
            position: relative;
            border-bottom: 1px dashed var(--border-subtle);
        }

        .quick-start-list li:last-child {
            border-bottom: none;
        }

        .quick-start-list li::before {
            content: '✓';
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 18px;
            height: 18px;
            background: linear-gradient(135deg, var(--primary-start), var(--primary-end));
            border-radius: 50%;
            font-size: 0.7rem;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
        }

        .quick-start-list strong {
            color: var(--text-primary);
            font-weight: 600;
        }

        /* Sidebar Footer */
        .sidebar-footer {
            margin-top: auto;
            padding-top: 24px;
            border-top: 1px solid var(--border-subtle);
            text-align: center;
        }

        .sidebar-footer p {
            font-size: 0.8rem;
            color: var(--text-muted);
            line-height: 1.8;
        }

        .sidebar-footer .version {
            display: inline-block;
            margin-top: 8px;
            padding: 4px 12px;
            background: rgba(124, 58, 237, 0.2);
            border-radius: var(--radius-full);
            font-size: 0.75rem;
            color: var(--text-accent);
        }

        /* Main Content */
        .main-content {
            flex: 1;
            margin-left: 320px;
            padding: 40px;
            min-height: 100vh;
        }

        /* Header */
        .page-header {
            text-align: center;
            max-width: 800px;
            margin: 0 auto 48px;
        }

        .brand-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 20px;
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.2), rgba(59, 130, 246, 0.15));
            border: 1px solid var(--bg-card-border);
            border-radius: var(--radius-full);
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-accent);
            margin-bottom: 20px;
            animation: badgeFloat 3s ease-in-out infinite;
        }

        @keyframes badgeFloat {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-4px); }
        }

        .page-title {
            font-family: 'Poppins', sans-serif;
            font-size: 3.5rem;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 16px;
            background: linear-gradient(135deg, #ffffff 0%, var(--text-accent) 50%, var(--primary-start) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: titleGlow 4s ease-in-out infinite;
        }

        @keyframes titleGlow {
            0%, 100% { filter: brightness(1); }
            50% { filter: brightness(1.1); }
        }

        .page-subtitle {
            font-size: 1.2rem;
            color: var(--text-secondary);
            font-weight: 400;
            max-width: 600px;
            margin: 0 auto;
        }

        /* Stats Row */
        .stats-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 16px;
            margin-bottom: 48px;
        }

        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--bg-card-border);
            border-radius: var(--radius-lg);
            padding: 24px 20px;
            text-align: center;
            transition: all var(--transition-normal);
            position: relative;
            overflow: hidden;
        }

        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary-start), var(--secondary-end));
            opacity: 0;
            transition: opacity var(--transition-fast);
        }

        .stat-card:hover {
            transform: translateY(-4px);
            border-color: var(--primary-start);
            box-shadow: var(--shadow-md);
        }

        .stat-card:hover::before {
            opacity: 1;
        }

        .stat-card .number {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary-start), var(--secondary-end));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 4px;
        }

        .stat-card .label {
            font-size: 0.9rem;
            color: var(--text-secondary);
            font-weight: 500;
        }

        /* Divider */
        .divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--border-subtle), transparent);
            margin: 48px 0;
            border: none;
        }

        /* Tabs */
        .tabs-wrapper {
            margin-bottom: 32px;
        }

        .tabs-header {
            display: flex;
            gap: 4px;
            padding: 6px;
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            margin-bottom: 24px;
            max-width: fit-content;
            margin-left: auto;
            margin-right: auto;
        }

        .tab-btn {
            flex: 1;
            padding: 14px 28px;
            background: transparent;
            border: none;
            border-radius: var(--radius-md);
            color: var(--text-secondary);
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            transition: all var(--transition-fast);
            position: relative;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .tab-btn::before {
            content: '';
            position: absolute;
            bottom: -1px;
            left: 50%;
            transform: translateX(-50%) scaleX(0);
            width: 80%;
            height: 2px;
            background: linear-gradient(90deg, var(--primary-start), var(--primary-end));
            border-radius: 2px;
            transition: transform var(--transition-fast);
        }

        .tab-btn:hover:not(.active) {
            color: var(--text-primary);
            background: rgba(255, 255, 255, 0.05);
        }

        .tab-btn.active {
            color: var(--text-primary);
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.3), rgba(59, 130, 246, 0.2));
            border: 1px solid var(--bg-card-border);
        }

        .tab-btn.active::before {
            transform: translateX(-50%) scaleX(1);
        }

        .tab-content {
            display: none;
            animation: fadeInUp 0.4s ease;
        }

        .tab-content.active {
            display: block;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Feature Cards */
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 16px;
        }

        .feature-card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 24px;
            cursor: pointer;
            transition: all var(--transition-normal);
            position: relative;
            overflow: hidden;
        }

        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.1), transparent 50%);
            opacity: 0;
            transition: opacity var(--transition-fast);
            pointer-events: none;
        }

        .feature-card:hover,
        .feature-card.selected {
            transform: translateY(-4px);
            border-color: var(--primary-start);
            box-shadow: var(--shadow-md);
        }

        .feature-card:hover::before,
        .feature-card.selected::before {
            opacity: 1;
        }

        .feature-card.selected {
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.15), rgba(59, 130, 246, 0.1));
            border-color: var(--primary-start);
        }

        .feature-card-icon {
            width: 44px;
            height: 44px;
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.3), rgba(59, 130, 246, 0.2));
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            margin-bottom: 14px;
            transition: transform var(--transition-fast);
        }

        .feature-card:hover .feature-card-icon {
            transform: scale(1.1);
        }

        .feature-card-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 8px;
        }

        .feature-card-desc {
            font-size: 0.9rem;
            color: var(--text-secondary);
            line-height: 1.5;
        }

        /* Tool Selector */
        .tool-select-wrapper {
            margin: 32px 0;
            text-align: center;
        }

        .tool-select-label {
            display: block;
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-accent);
            margin-bottom: 14px;
        }

        .tool-select {
            width: 100%;
            max-width: 500px;
            padding: 16px 20px;
            background: var(--bg-card);
            border: 2px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            color: var(--text-primary);
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: all var(--transition-fast);
            appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23c4b5fd' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 16px center;
            background-size: 20px;
            padding-right: 48px;
        }

        .tool-select:focus {
            outline: none;
            border-color: var(--border-focus);
            box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.2);
        }

        /* Input Section */
        .input-section {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-xl);
            padding: 32px;
            margin-bottom: 32px;
        }

        .input-section-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .input-section-title::after {
            content: '';
            flex: 1;
            height: 1px;
            background: var(--border-subtle);
        }

        .input-group {
            margin-bottom: 20px;
        }

        .input-group:last-child {
            margin-bottom: 0;
        }

        .input-label {
            display: block;
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 10px;
        }

        .input-field {
            width: 100%;
            padding: 16px 20px;
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid var(--border-subtle);
            border-radius: var(--radius-md);
            color: var(--text-primary);
            font-size: 1rem;
            font-family: inherit;
            transition: all var(--transition-fast);
            resize: vertical;
        }

        .input-field:focus {
            outline: none;
            border-color: var(--border-focus);
            box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.2);
            background: rgba(255, 255, 255, 0.08);
        }

        .input-field::placeholder {
            color: var(--text-muted);
        }

        textarea.input-field {
            min-height: 140px;
            line-height: 1.6;
        }

        /* Advanced Options */
        .advanced-section {
            background: rgba(124, 58, 237, 0.08);
            border: 1px solid rgba(124, 58, 237, 0.3);
            border-radius: var(--radius-lg);
            padding: 24px;
            margin-bottom: 32px;
        }

        .advanced-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            cursor: pointer;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-subtle);
            margin-bottom: 20px;
        }

        .advanced-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .advanced-toggle {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: rgba(124, 58, 237, 0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-accent);
            transition: transform var(--transition-fast);
            font-size: 1.2rem;
        }

        .advanced-toggle.collapsed {
            transform: rotate(-90deg);
        }

        .advanced-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
        }

        .advanced-option {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .advanced-option label {
            font-size: 0.9rem;
            color: var(--text-secondary);
            font-weight: 500;
        }

        .advanced-option select,
        .advanced-option input[type="range"] {
            width: 100%;
            padding: 12px 16px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-sm);
            color: var(--text-primary);
            font-size: 0.95rem;
            cursor: pointer;
            transition: all var(--transition-fast);
        }

        .advanced-option select {
            appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23a1a1aa' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 12px center;
            background-size: 16px;
            padding-right: 36px;
        }

        .advanced-option select:focus,
        .advanced-option input[type="range"]:focus {
            outline: none;
            border-color: var(--border-focus);
        }

        .range-display {
            text-align: right;
            font-size: 0.85rem;
            color: var(--primary-start);
            font-weight: 600;
            margin-top: 4px;
        }

        /* Generate Button */
        .generate-wrapper {
            text-align: center;
            margin: 40px 0;
        }

        .generate-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            padding: 18px 56px;
            background: linear-gradient(135deg, var(--primary-start), var(--primary-end));
            color: white;
            font-size: 1.1rem;
            font-weight: 700;
            border: none;
            border-radius: var(--radius-full);
            cursor: pointer;
            transition: all var(--transition-normal);
            box-shadow: var(--shadow-glow);
            position: relative;
            overflow: hidden;
            min-width: 340px;
        }

        .generate-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }

        .generate-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 50px var(--primary-glow);
        }

        .generate-btn:hover::before {
            left: 100%;
        }

        .generate-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }

        .generate-btn:disabled:hover::before {
            left: -100%;
        }

        .generate-btn.pulse {
            animation: btnPulse 2s infinite;
        }

        @keyframes btnPulse {
            0% { box-shadow: 0 0 0 0 var(--primary-glow); }
            70% { box-shadow: 0 0 0 20px rgba(124, 58, 237, 0); }
            100% { box-shadow: 0 0 0 0 rgba(124, 58, 237, 0); }
        }

        /* Progress */
        .progress-wrapper {
            display: none;
            max-width: 600px;
            margin: 0 auto 40px;
        }

        .progress-wrapper.active {
            display: block;
            animation: fadeInUp 0.4s ease;
        }

        .progress-status {
            text-align: center;
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-accent);
            margin-bottom: 16px;
            min-height: 24px;
        }

        .progress-bar {
            height: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: var(--radius-full);
            overflow: hidden;
            position: relative;
        }

        .progress-bar::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 1.5s infinite;
        }

        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary-start), var(--secondary-end));
            border-radius: var(--radius-full);
            width: 0%;
            transition: width 0.4s ease;
            position: relative;
        }

        .progress-fill::after {
            content: '';
            position: absolute;
            top: -2px;
            right: -2px;
            width: 6px;
            height: 12px;
            background: white;
            border-radius: 3px;
            box-shadow: 0 0 10px rgba(255,255,255,0.8);
            opacity: 0;
            transition: opacity 0.2s;
        }

        .progress-fill.active::after {
            opacity: 1;
        }

        /* Results */
        .results-wrapper {
            display: none;
            animation: fadeInUp 0.5s ease;
        }

        .results-wrapper.active {
            display: block;
        }

        .success-banner {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.1));
            border: 1px solid rgba(16, 185, 129, 0.4);
            border-left: 4px solid var(--success);
            border-radius: var(--radius-md);
            padding: 16px 24px;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 500;
            color: var(--success);
        }

        .result-badge {
            text-align: center;
            margin-bottom: 24px;
        }

        .result-badge span {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 24px;
            background: rgba(124, 58, 237, 0.2);
            border: 1px solid var(--bg-card-border);
            border-radius: var(--radius-full);
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-accent);
        }

        .result-box {
            background: linear-gradient(145deg, rgba(30, 30, 50, 0.8), rgba(20, 20, 40, 0.9));
            border: 1px solid var(--bg-card-border);
            border-radius: var(--radius-xl);
            padding: 32px;
            color: var(--text-primary);
            font-size: 1.05rem;
            line-height: 1.8;
            margin-bottom: 32px;
            white-space: pre-wrap;
            overflow-y: auto;
            max-height: 650px;
            box-shadow: var(--shadow-lg);
        }

        .result-box h1, .result-box h2, .result-box h3, .result-box h4 {
            color: var(--text-accent);
            margin: 1.5rem 0 1rem;
            font-weight: 700;
        }

        .result-box h1 { font-size: 1.9rem; }
        .result-box h2 { font-size: 1.6rem; }
        .result-box h3 { font-size: 1.35rem; }
        .result-box h4 { font-size: 1.15rem; }

        .result-box ul, .result-box ol {
            margin: 1rem 0 1rem 24px;
        }

        .result-box li {
            margin-bottom: 0.5rem;
        }

        .result-box strong {
            color: var(--primary-start);
            font-weight: 600;
        }

        .result-box code {
            background: rgba(124, 58, 237, 0.2);
            padding: 2px 8px;
            border-radius: 4px;
            font-family: 'Fira Code', monospace;
            font-size: 0.95em;
        }

        /* Export Section */
        .export-section {
            margin-top: 40px;
        }

        .export-section-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .export-section-title::after {
            content: '';
            flex: 1;
            height: 1px;
            background: var(--border-subtle);
        }

        .export-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .export-card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 24px;
        }

        .export-card-title {
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .export-textarea {
            width: 100%;
            min-height: 220px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 14px 16px;
            color: var(--text-primary);
            font-family: inherit;
            font-size: 0.95rem;
            resize: vertical;
            line-height: 1.6;
        }

        .export-textarea:focus {
            outline: none;
            border-color: var(--border-focus);
        }

        .export-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 16px;
        }

        .export-btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 20px;
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.3), rgba(59, 130, 246, 0.2));
            color: var(--text-primary);
            border: 1px solid var(--bg-card-border);
            border-radius: var(--radius-md);
            font-weight: 600;
            font-size: 0.95rem;
            cursor: pointer;
            transition: all var(--transition-fast);
        }

        .export-btn:hover {
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.4), rgba(59, 130, 246, 0.3));
            border-color: var(--primary-start);
            transform: translateY(-2px);
        }

        .tips-card {
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.3);
        }

        .tips-list {
            list-style: none;
            font-size: 0.9rem;
            color: var(--text-secondary);
            line-height: 1.8;
        }

        .tips-list li {
            padding-left: 20px;
            position: relative;
        }

        .tips-list li::before {
            content: '💡';
            position: absolute;
            left: 0;
            top: 2px;
        }

        /* Messages */
        .message-box {
            padding: 18px 24px;
            border-radius: var(--radius-md);
            margin: 20px 0;
            border-left: 4px solid;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .message-box.error {
            background: rgba(239, 68, 68, 0.1);
            border-color: var(--error);
            color: #fca5a5;
        }

        .message-box.warning {
            background: rgba(245, 158, 11, 0.1);
            border-color: var(--warning);
            color: #fcd34d;
        }

        .message-box.info {
            background: rgba(59, 130, 246, 0.1);
            border-color: var(--info);
            color: #93c5fd;
        }

        .message-box.success {
            background: rgba(16, 185, 129, 0.1);
            border-color: var(--success);
            color: #6ee7b7;
        }

        .message-box h4 {
            margin-bottom: 6px;
            font-weight: 600;
        }

        .message-box ul, .message-box ol {
            margin-left: 20px;
            margin-top: 8px;
        }

        .message-box a {
            color: var(--primary-start);
            text-decoration: none;
        }

        .message-box a:hover {
            text-decoration: underline;
        }

        /* Footer */
        .page-footer {
            text-align: center;
            padding: 48px 20px 32px;
            margin-top: 40px;
            border-top: 1px solid var(--border-subtle);
        }

        .footer-brand {
            font-family: 'Poppins', sans-serif;
            font-size: 1.4rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary-start), var(--secondary-end));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
        }

        .footer-text {
            color: var(--text-muted);
            font-size: 0.95rem;
            line-height: 1.8;
        }

        /* Mobile Toggle */
        .mobile-toggle {
            display: none;
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 200;
            width: 48px;
            height: 48px;
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            color: var(--text-primary);
            font-size: 1.4rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all var(--transition-fast);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }

        .mobile-toggle:hover {
            background: var(--bg-surface-hover);
            border-color: var(--primary-start);
        }

        .overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px);
            z-index: 90;
        }

        .overlay.active {
            display: block;
        }

        /* Responsive */
        @media (max-width: 1200px) {
            .sidebar {
                transform: translateX(-100%);
                box-shadow: var(--shadow-lg);
            }
            .sidebar.open {
                transform: translateX(0);
            }
            .main-content {
                margin-left: 0;
                padding: 24px 20px;
                padding-top: 80px;
            }
            .mobile-toggle {
                display: flex;
            }
            .page-title {
                font-size: 2.8rem;
            }
        }

        @media (max-width: 768px) {
            .page-title {
                font-size: 2.3rem;
            }
            .page-subtitle {
                font-size: 1.05rem;
            }
            .stats-row {
                grid-template-columns: repeat(2, 1fr);
            }
            .tabs-header {
                flex-wrap: wrap;
            }
            .tab-btn {
                padding: 12px 16px;
                font-size: 0.9rem;
            }
            .feature-grid {
                grid-template-columns: 1fr;
            }
            .generate-btn {
                width: 100%;
                min-width: unset;
                padding: 16px 32px;
            }
            .input-section,
            .advanced-section,
            .export-card {
                padding: 24px 20px;
            }
            .result-box {
                padding: 24px 20px;
                font-size: 1rem;
            }
            .advanced-grid {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 480px) {
            .stats-row {
                grid-template-columns: 1fr;
            }
            .stat-card .number {
                font-size: 1.8rem;
            }
            .logo-text {
                font-size: 1.5rem;
            }
            .page-header {
                margin-bottom: 32px;
            }
            .divider {
                margin: 32px 0;
            }
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: var(--bg-base);
        }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, var(--primary-start), var(--primary-end));
            border-radius: 4px;
            border: 2px solid var(--bg-base);
        }
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, var(--primary-end), var(--secondary-end));
        }

        /* Focus visible for accessibility */
        :focus-visible {
            outline: 2px solid var(--primary-start);
            outline-offset: 2px;
        }

        /* Reduced motion */
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }
    </style>
</head>
<body>
    <!-- Animated Particles -->
    <div class="particles" id="particles"></div>

    <!-- Mobile Toggle -->
    <button class="mobile-toggle" onclick="toggleSidebar()" aria-label="Toggle menu">☰</button>
    <div class="overlay" onclick="toggleSidebar()"></div>

    <div class="app-wrapper">
        <!-- Sidebar -->
        <aside class="sidebar" id="sidebar">
            <div class="sidebar-header">
                <div class="logo">
                    <div class="logo-icon">🎬</div>
                    <div class="logo-text">SemTube</div>
                </div>
                <div class="logo-tagline">AI YouTube Empire</div>
            </div>

            <div class="sidebar-section">
                <div class="sidebar-section-title">🔐 API Access</div>
                <div class="api-card">
                    <input type="password" id="apiKey" class="api-input" placeholder="Paste your Gemini API key..." oninput="updateApiStatus()">
                </div>
                <div class="api-card">
                    <input type="text" id="transcriptProxy" class="api-input" placeholder="CORS Proxy (optional)" value="https://corsproxy.io/?">
                </div>
                <span class="status-pill inactive" id="apiStatus">⚠️ Add API Key to begin</span>
                <p class="api-hint">
                    🆓 Get your FREE key at 
                    <a href="https://aistudio.google.com" target="_blank" rel="noopener">aistudio.google.com</a>
                </p>
            </div>

            <div class="sidebar-section">
                <div class="sidebar-section-title">📊 Platform Stats</div>
                <div class="stats-grid">
                    <div class="stat-card-mini">
                        <div class="stat-value">10</div>
                        <div class="stat-label">AI Tools</div>
                    </div>
                    <div class="stat-card-mini">
                        <div class="stat-value">∞</div>
                        <div class="stat-label">Generations</div>
                    </div>
                    <div class="stat-card-mini">
                        <div class="stat-value">$0</div>
                        <div class="stat-label">Forever Free</div>
                    </div>
                    <div class="stat-card-mini">
                        <div class="stat-value">5+</div>
                        <div class="stat-label">Languages</div>
                    </div>
                </div>
            </div>

            <div class="sidebar-section">
                <div class="sidebar-section-title">🚀 Quick Start</div>
                <ul class="quick-start-list">
                    <li><strong>Get API Key</strong> from Google AI Studio</li>
                    <li><strong>Paste Key</strong> in the field above</li>
                    <li><strong>Select Tool</strong> from the options</li>
                    <li><strong>Enter Topic</strong> or YouTube URL</li>
                    <li><strong>Generate</strong> & copy your content!</li>
                </ul>
            </div>

            <div class="sidebar-footer">
                <p>Powered by Google Gemini AI<br>Built with ❤️ for creators</p>
                <span class="version">v3.0 • 2026</span>
            </div>
        </aside>

        <!-- Main Content -->
        <main class="main-content">
            <header class="page-header">
                <div class="brand-badge">✨ SemTube AI Studio</div>
                <h1 class="page-title">Build Your YouTube Empire</h1>
                <p class="page-subtitle">10 Professional AI Tools • Zero Cost • Instant Results</p>
            </header>

            <!-- Stats Row -->
            <div class="stats-row">
                <div class="stat-card">
                    <div class="number">10</div>
                    <div class="label">Pro AI Tools</div>
                </div>
                <div class="stat-card">
                    <div class="number">∞</div>
                    <div class="label">Unlimited Use</div>
                </div>
                <div class="stat-card">
                    <div class="number">$0</div>
                    <div class="label">100% Free</div>
                </div>
                <div class="stat-card">
                    <div class="number">5</div>
                    <div class="label">Languages</div>
                </div>
            </div>

            <hr class="divider">

            <!-- Tool Tabs -->
            <div class="tabs-wrapper">
                <div class="tabs-header" role="tablist">
                    <button class="tab-btn active" onclick="switchTab('content')" role="tab" aria-selected="true">
                        📝 Content
                    </button>
                    <button class="tab-btn" onclick="switchTab('seo')" role="tab">
                        🔍 SEO
                    </button>
                    <button class="tab-btn" onclick="switchTab('advanced')" role="tab">
                        🎬 Advanced
                    </button>
                </div>

                <!-- Content Tab -->
                <div class="tab-content active" id="tab-content" role="tabpanel">
                    <div class="feature-grid">
                        <div class="feature-card" data-tool="viral" onclick="selectTool('viral')">
                            <div class="feature-card-icon">🔥</div>
                            <h4 class="feature-card-title">Viral Ideas</h4>
                            <p class="feature-card-desc">10 trending video concepts with viral potential analysis</p>
                        </div>
                        <div class="feature-card" data-tool="script" onclick="selectTool('script')">
                            <div class="feature-card-icon">📜</div>
                            <h4 class="feature-card-title">Video Script</h4>
                            <p class="feature-card-desc">Complete script with hook, body, CTA & outro structure</p>
                        </div>
                        <div class="feature-card" data-tool="thumbnail" onclick="selectTool('thumbnail')">
                            <div class="feature-card-icon">🎯</div>
                            <h4 class="feature-card-title">Thumbnail Text</h4>
                            <p class="feature-card-desc">Bold, clickable text suggestions for max CTR</p>
                        </div>
                        <div class="feature-card" data-tool="comments" onclick="selectTool('comments')">
                            <div class="feature-card-icon">💬</div>
                            <h4 class="feature-card-title">Comment Replies</h4>
                            <p class="feature-card-desc">Smart templates for positive, negative & question comments</p>
                        </div>
                    </div>
                </div>

                <!-- SEO Tab -->
                <div class="tab-content" id="tab-seo" role="tabpanel">
                    <div class="feature-grid">
                        <div class="feature-card" data-tool="title" onclick="selectTool('title')">
                            <div class="feature-card-icon">🏷️</div>
                            <h4 class="feature-card-title">Title Generator</h4>
                            <p class="feature-card-desc">10 high-CTR titles with power words & curiosity hooks</p>
                        </div>
                        <div class="feature-card" data-tool="description" onclick="selectTool('description')">
                            <div class="feature-card-icon">📝</div>
                            <h4 class="feature-card-title">SEO Description</h4>
                            <p class="feature-card-desc">Optimized description with keywords, timestamps & hashtags</p>
                        </div>
                        <div class="feature-card" data-tool="tags" onclick="selectTool('tags')">
                            <div class="feature-card-icon">🔖</div>
                            <h4 class="feature-card-title">Trending Tags</h4>
                            <p class="feature-card-desc">30 researched tags: broad, specific & long-tail keywords</p>
                        </div>
                        <div class="feature-card" data-tool="keywords" onclick="selectTool('keywords')">
                            <div class="feature-card-icon">📊</div>
                            <h4 class="feature-card-title">Keyword Research</h4>
                            <p class="feature-card-desc">High-volume, low-competition keywords with intent analysis</p>
                        </div>
                    </div>
                </div>

                <!-- Advanced Tab -->
                <div class="tab-content" id="tab-advanced" role="tabpanel">
                    <div class="feature-grid">
                        <div class="feature-card" data-tool="summarizer" onclick="selectTool('summarizer')">
                            <div class="feature-card-icon">📹</div>
                            <h4 class="feature-card-title">Video Summarizer</h4>
                            <p class="feature-card-desc">Paste any YouTube URL for instant AI-powered summary</p>
                        </div>
                        <div class="feature-card" data-tool="hooks" onclick="selectTool('hooks')">
                            <div class="feature-card-icon">🎤</div>
                            <h4 class="feature-card-title">Hook Generator</h4>
                            <p class="feature-card-desc">10 scroll-stopping hooks for the critical first 5 seconds</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tool Selector -->
            <div class="tool-select-wrapper">
                <label class="tool-select-label" for="mainToolSelect">🎯 Active Tool</label>
                <select class="tool-select" id="mainToolSelect" onchange="updateToolSelection(this.value)">
                    <option value="viral">🔥 Viral Video Ideas Generator</option>
                    <option value="script">📜 Full Video Script Writer</option>
                    <option value="thumbnail">🎯 Thumbnail Text Suggestions</option>
                    <option value="comments">💬 Comment Reply Generator</option>
                    <option value="title">🏷️ Title Generator (10 Variants)</option>
                    <option value="description">📝 SEO Description Writer</option>
                    <option value="tags">🔖 Trending Tags Finder</option>
                    <option value="keywords">📊 Keyword Research Tool</option>
                    <option value="summarizer">📹 YouTube Video Summarizer</option>
                    <option value="hooks">🎤 Hook Generator (First 5 Sec)</option>
                </select>
            </div>

            <hr class="divider">

            <!-- Input Section -->
            <section class="input-section">
                <h3 class="input-section-title">✍️ Your Input</h3>
                <div id="inputContainer">
                    <div class="input-group" id="topicInput">
                        <label class="input-label" for="userInput">Topic / Niche / Keyword</label>
                        <textarea id="userInput" class="input-field" placeholder="e.g., How to make money with AI in 2026, Best productivity apps for students..."></textarea>
                    </div>
                    <div class="input-group" id="urlInput" style="display: none;">
                        <label class="input-label" for="userUrl">YouTube Video URL</label>
                        <input type="text" id="userUrl" class="input-field" placeholder="https://www.youtube.com/watch?v=xxxxx">
                    </div>
                </div>
            </section>

            <!-- Advanced Options -->
            <section class="advanced-section">
                <div class="advanced-header" onclick="toggleAdvanced()">
                    <div class="advanced-title">⚙️ Advanced Settings</div>
                    <div class="advanced-toggle" id="advancedToggle">▼</div>
                </div>
                <div class="advanced-grid" id="advancedContent">
                    <div class="advanced-option">
                        <label for="tone">Content Tone</label>
                        <select id="tone">
                            <option>Professional</option>
                            <option>Casual & Friendly</option>
                            <option>Funny & Entertaining</option>
                            <option>Educational</option>
                            <option>Motivational</option>
                            <option>Dramatic</option>
                        </select>
                    </div>
                    <div class="advanced-option">
                        <label for="language">Language</label>
                        <select id="language">
                            <option>English</option>
                            <option>Bengali (বাংলা)</option>
                            <option>Hinglish</option>
                            <option>Hindi</option>
                            <option>Mix (English + Bengali)</option>
                        </select>
                    </div>
                    <div class="advanced-option">
                        <label for="audience">Target Audience</label>
                        <select id="audience">
                            <option>General</option>
                            <option>Students</option>
                            <option>Professionals</option>
                            <option>Beginners</option>
                            <option>Tech Enthusiasts</option>
                            <option>Business Owners</option>
                        </select>
                    </div>
                    <div class="advanced-option">
                        <label for="length">Content Length: <span id="lengthValue">300</span> words</label>
                        <input type="range" id="length" min="100" max="1000" value="300" step="50" oninput="document.getElementById('lengthValue').textContent=this.value">
                    </div>
                </div>
            </section>

            <!-- Generate Button -->
            <div class="generate-wrapper">
                <button class="generate-btn" id="generateBtn" onclick="generateContent()">
                    <span>🚀</span> Generate with SemTube AI
                </button>
            </div>

            <!-- Progress -->
            <div class="progress-wrapper" id="progressContainer">
                <div class="progress-status" id="progressText">🧠 Initializing AI Engine...</div>
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
            </div>

            <!-- Results -->
            <div class="results-wrapper" id="resultsContainer">
                <div class="success-banner">✅ Content generated successfully!</div>
                <div class="result-badge" id="resultBadge"></div>
                
                <div class="result-box" id="resultBox"></div>

                <!-- Export Section -->
                <section class="export-section">
                    <h3 class="export-section-title">📥 Export Options</h3>
                    <div class="export-grid">
                        <div class="export-card">
                            <h4 class="export-card-title">📋 Copy-Friendly</h4>
                            <textarea id="exportTextarea" class="export-textarea" readonly></textarea>
                        </div>
                        <div class="export-card">
                            <h4 class="export-card-title">💾 Download</h4>
                            <div class="export-actions">
                                <button class="export-btn" onclick="downloadTXT()">📥 .TXT</button>
                                <button class="export-btn" onclick="downloadMD()">📄 .MD</button>
                            </div>
                        </div>
                        <div class="export-card tips-card">
                            <h4 class="export-card-title">💡 Pro Tips</h4>
                            <ul class="tips-list">
                                <li>Personalize AI content with your unique voice</li>
                                <li>Test different tones for best engagement</li>
                                <li>Combine tools for complete workflow</li>
                                <li>Regenerate for fresh variations anytime</li>
                            </ul>
                        </div>
                    </div>
                </section>

                <div class="message-box info">
                    🔄 <strong>Want different results?</strong> Adjust tone, language, or rephrase your topic and generate again!
                </div>
            </div>

            <!-- Footer -->
            <footer class="page-footer">
                <div class="footer-brand">SemTube AI</div>
                <p class="footer-text">
                    Your Complete YouTube Automation Companion<br>
                    Powered by Google Gemini AI • 2026 Edition
                </p>
            </footer>
        </main>
    </div>

    <script>
        // Create floating particles
        function createParticles() {
            const container = document.getElementById('particles');
            const particleCount = 25;
            
            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 15 + 's';
                particle.style.animationDuration = (15 + Math.random() * 10) + 's';
                particle.style.width = (2 + Math.random() * 4) + 'px';
                particle.style.height = particle.style.width;
                particle.style.opacity = 0.2 + Math.random() * 0.4;
                container.appendChild(particle);
            }
        }

        // State
        let currentTool = 'viral';
        let generatedText = '';

        // Tool names mapping
        const toolNames = {
            viral: '🔥 Viral Video Ideas Generator',
            script: '📜 Full Video Script Writer',
            thumbnail: '🎯 Thumbnail Text Suggestions',
            comments: '💬 Comment Reply Generator',
            title: '🏷️ Title Generator (10 Variants)',
            description: '📝 SEO Description Writer',
            tags: '🔖 Trending Tags Finder',
            keywords: '📊 Keyword Research Tool',
            summarizer: '📹 YouTube Video Summarizer',
            hooks: '🎤 Hook Generator (First 5 Sec)'
        };

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            createParticles();
            selectTool('viral');
        });

        // UI Functions
        function updateApiStatus() {
            const key = document.getElementById('apiKey').value.trim();
            const status = document.getElementById('apiStatus');
            if (key.length > 10) {
                status.className = 'status-pill active';
                status.textContent = '✅ API Connected';
            } else {
                status.className = 'status-pill inactive';
                status.textContent = '⚠️ Add API Key to begin';
            }
        }

        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('open');
            document.querySelector('.overlay').classList.toggle('active');
        }

        function switchTab(tab) {
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
                btn.setAttribute('aria-selected', 'false');
            });
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            event.currentTarget.classList.add('active');
            event.currentTarget.setAttribute('aria-selected', 'true');
            document.getElementById(`tab-${tab}`).classList.add('active');
        }

        function selectTool(tool) {
            currentTool = tool;
            document.getElementById('mainToolSelect').value = tool;
            
            // Update visual selection
            document.querySelectorAll('.feature-card').forEach(card => {
                card.classList.remove('selected');
                if (card.dataset.tool === tool) card.classList.add('selected');
            });

            updateToolSelection(tool);
        }

        function updateToolSelection(tool) {
            currentTool = tool;
            
            // Show/hide appropriate input
            const topicInput = document.getElementById('topicInput');
            const urlInput = document.getElementById('urlInput');
            
            if (tool === 'summarizer') {
                topicInput.style.display = 'none';
                urlInput.style.display = 'block';
            } else {
                topicInput.style.display = 'block';
                urlInput.style.display = 'none';
            }

            // Update feature cards
            document.querySelectorAll('.feature-card').forEach(card => {
                card.classList.remove('selected');
                if (card.dataset.tool === tool) card.classList.add('selected');
            });
        }

        function toggleAdvanced() {
            const content = document.getElementById('advancedContent');
            const toggle = document.getElementById('advancedToggle');
            const isHidden = content.style.display === 'none';
            
            content.style.display = isHidden ? 'grid' : 'none';
            toggle.classList.toggle('collapsed', !isHidden);
        }

        // Prompt Generation
        function getPrompt(tool, input, tone, language, audience, length) {
            const prompts = {
                viral: `You are a top YouTube strategist with 10+ years of experience growing channels from 0 to millions.

Generate 10 highly viral and unique YouTube video ideas about: '${input}'

Target Audience: ${audience}
Tone: ${tone}
Language: ${language}

For EACH idea, provide:
📌 **Video Title**: (Catchy, click-worthy, under 60 chars)
📝 **Brief Description**: (2-3 lines explaining the concept)
🎯 **Why It Will Go Viral**: (1 line - psychological trigger)
📊 **Estimated Difficulty**: (Easy / Medium / Hard to produce)
💰 **Monetization Potential**: (Low / Medium / High)

Format each idea clearly with numbers 1-10.
Make each idea UNIQUE - no repetition!
Focus on ideas that can realistically go viral in 2026.`,

                script: `You are a professional YouTube scriptwriter who has written scripts for channels with millions of subscribers.

Write a complete, highly engaging YouTube video script about: '${input}'

Target Audience: ${audience}
Tone: ${tone}  
Language: ${language}
Approximate Length: ${length} words

SCRIPT STRUCTURE:

🎣 **HOOK (0-5 seconds)**:
Write an attention-grabbing opening that makes viewers STOP scrolling. Use curiosity, shock value, or a bold claim.

📢 **INTRO (5-30 seconds)**:
- Introduce the topic
- State the problem/opportunity
- Tell viewers what they'll learn
- Build credibility

📚 **MAIN CONTENT (Body)**:
- Break into 3-5 clear sections/points
- Use storytelling and examples
- Include transitions between points
- Add "Pattern Interrupts" every 60-90 seconds (to maintain retention)
- Include viewer engagement prompts ("Comment below if...")

🔔 **CALL TO ACTION (Before Outro)**:
- Ask to subscribe with specific reason
- Like reminder
- Comment prompt with specific question
- Share request

👋 **OUTRO (Last 15-20 seconds)**:
- Summarize key takeaway
- Tease next video
- End with memorable closing line

FORMATTING RULES:
- Use [B-ROLL] markers for visual suggestions
- Use [SHOW ON SCREEN] for text/graphic suggestions
- Use [PAUSE] for dramatic effect
- Write in conversational, spoken language
- Add emotion cues [ENTHUSIASTIC], [SERIOUS], [WHISPER] etc.

Make it feel natural, NOT robotic!`,

                title: `You are a YouTube SEO expert who specializes in creating high-CTR titles that rank #1 in search.

Generate 10 unique, high-performing YouTube video titles about: '${input}'

Language: ${language}
Tone: ${tone}

REQUIREMENTS FOR EACH TITLE:
✅ Under 60 characters (STRICT)
✅ Include at least ONE power word (Free, Secret, Proven, Ultimate, Insane, etc.)
✅ Use numbers where possible
✅ Create a curiosity gap
✅ Must make someone NEED to click

TITLE CATEGORIES (create variety):
1-2: Number-based titles ("7 Ways...", "Top 5...")
3-4: How-to titles ("How to..." "How I...")
5-6: Curiosity/Mystery titles ("The Secret...", "Nobody Tells You...")
7-8: Urgency titles ("Stop Doing This!", "Before It's Too Late...")
9-10: Bold/Controversial titles ("I Was Wrong About...", "The Truth About...")

For each title also provide:
📊 **Estimated CTR Potential**: ⭐⭐⭐⭐⭐ (rate 1-5)
🎯 **Best For**: (Search / Browse / Both)

Format as numbered list 1-10.`,

                description: `You are a YouTube SEO specialist who has helped 500+ channels rank on page 1.

Write a fully SEO-optimized YouTube video description about: '${input}'

Language: ${language}
Tone: ${tone}

DESCRIPTION STRUCTURE:

📌 **FIRST 2 LINES (Above the fold - MOST IMPORTANT):**
- Hook with main keyword naturally included
- This appears in search results, make it compelling!
- Under 150 characters

📝 **PARAGRAPH 2 (Detailed Overview):**
- 3-4 sentences explaining what the video covers
- Include 3-5 relevant keywords naturally
- Add value proposition

⏱️ **TIMESTAMPS:**
0:00 - Introduction
[Generate 5-8 realistic timestamps based on topic]

🔗 **RESOURCES & LINKS:**
📌 [Resource 1 mentioned in video]
📌 [Resource 2 mentioned in video]
📌 Free Download: [Placeholder]

📱 **SOCIAL MEDIA:**
📸 Instagram: @[your-handle]
🐦 Twitter: @[your-handle]
💼 LinkedIn: [your-profile]
🌐 Website: [your-website]

📧 **BUSINESS INQUIRIES:**
Email: [your-email]

🏷️ **TAGS IN DESCRIPTION:**
#hashtag1 #hashtag2 #hashtag3 #hashtag4 #hashtag5

⚖️ **DISCLAIMER (if applicable):**
[Standard disclaimer text]

RULES:
- Use main keyword in first sentence
- Include 5-8 secondary keywords throughout
- Total length: 200-300 words
- Make it scannable with line breaks
- Include call-to-action to subscribe`,

                tags: `You are a YouTube algorithm expert who understands how tags affect video discovery and ranking.

Generate 30 highly effective, searchable tags for a YouTube video about: '${input}'

ORGANIZE INTO 3 CATEGORIES:

🔵 **BROAD TAGS (10 tags):**
- High search volume
- General terms related to the topic
- 1-2 word tags
- These help YouTube understand your content category

🟡 **MEDIUM-SPECIFIC TAGS (10 tags):**
- Moderate search volume  
- More specific to the exact topic
- 2-4 word phrases
- These help rank for specific searches

🟢 **LONG-TAIL TAGS (10 tags):**
- Lower competition
- Very specific phrases
- 4-7 word phrases
- These help you rank faster as a small channel

RULES:
- Each tag under 30 characters
- No duplicate concepts
- Mix singular and plural forms
- Include common misspellings if relevant
- Include trending variations

Also provide:
📊 **Tag Strategy Tip**: One paragraph about how to best use these tags
⚠️ **Tags to AVOID**: 3 tags that might seem relevant but would hurt performance`,

                keywords: `You are a YouTube keyword research expert with deep knowledge of search algorithms and trends.

Perform comprehensive YouTube keyword research for: '${input}'

Language: ${language}
Target Audience: ${audience}

PROVIDE:

📈 **1. HIGH VOLUME KEYWORDS (5 keywords):**
For each keyword:
- Keyword phrase
- Estimated Monthly Searches: High/Very High
- Competition Level: High
- Best content type: (Tutorial/Review/List/Vlog)
- Sample title using this keyword

📉 **2. LOW COMPETITION KEYWORDS (5 keywords):**
For each keyword:
- Keyword phrase
- Estimated Monthly Searches: Medium
- Competition Level: Low
- Why it's easy to rank for
- Sample title using this keyword

🎯 **3. LONG-TAIL KEYWORDS (5 keywords):**
For each keyword:
- Keyword phrase (4-7 words)
- Search Intent: (Informational/Commercial/Navigational)
- Competition Level: Very Low
- Best for: (New channels/Established channels)
- Sample title using this keyword

🔥 **4. TRENDING KEYWORDS (3 keywords):**
- Currently trending related terms
- Why they're trending
- Time sensitivity (Act now / Evergreen)

💡 **5. CONTENT GAP KEYWORDS (2 keywords):**
- Terms people search but few videos cover
- Opportunity analysis

📋 **STRATEGY RECOMMENDATION:**
One paragraph about which keywords to target first and why.`,

                hooks: `You are a YouTube retention expert who specializes in the critical first 5 seconds of a video.

Generate 10 POWERFUL hooks for a video about: '${input}'

Tone: ${tone}
Language: ${language}
Target Audience: ${audience}

REQUIREMENTS FOR EACH HOOK:
- Maximum 2 sentences (must be deliverable in 5 seconds)
- Must create immediate curiosity, shock, or perceived value
- Must make the viewer psychologically UNABLE to scroll away
- Must connect to the actual video content (no clickbait)

HOOK CATEGORIES:

🤯 **SHOCK HOOKS (2):**
Start with a surprising fact or statement

❓ **QUESTION HOOKS (2):**
Ask a question the viewer desperately wants answered

💰 **VALUE HOOKS (2):**
Promise specific, tangible value immediately

📖 **STORY HOOKS (2):**
Start with a mini-story or personal experience

⚡ **BOLD CLAIM HOOKS (2):**
Make a confident, specific claim

For each hook also provide:
🎭 **Delivery Tip**: How to say it (tone, speed, expression)
📊 **Retention Impact**: ⭐⭐⭐⭐⭐ (rate 1-5)

Make each hook UNIQUE and IMPOSSIBLE to resist!`,

                thumbnail: `You are a thumbnail design expert who has created thumbnails for videos with 10M+ views.

Generate 10 thumbnail text options for a video about: '${input}'

Tone: ${tone}

STRICT REQUIREMENTS:
- Maximum 3-4 WORDS per text (thumbnails need BIG readable text)
- Must be readable on a phone screen
- Must create curiosity or emotion
- Must complement (not repeat) the video title

TEXT CATEGORIES:

😱 **SHOCK/EMOTION (3 options):**
- Text that triggers emotional response
- Example style: "IT'S OVER" / "I QUIT" / "NOT AGAIN"

🔢 **NUMBER-BASED (3 options):**
- Include specific numbers for credibility
- Example style: "$10K/MONTH" / "IN 7 DAYS" / "100% FREE"

❓ **CURIOSITY (2 options):**
- Make viewer need to know more
- Example style: "DON'T DO THIS" / "FINALLY..." / "THE TRUTH"

🏆 **VALUE/BENEFIT (2 options):**
- Promise clear benefit
- Example style: "GAME CHANGER" / "EASY METHOD" / "IT WORKS"

For each text also suggest:
🎨 **Color**: Best text color for this specific text
📍 **Position**: Where to place on thumbnail (top-left, center, bottom-right, etc.)
✨ **Style**: Font style suggestion (Bold, Outline, 3D, etc.)
🖼️ **Background Suggestion**: What should be in the thumbnail image behind the text`,

                comments: `You are a YouTube community manager expert who knows how to boost engagement through strategic comment replies.

Generate smart comment reply templates for a video about: '${input}'

Tone: ${tone}
Language: ${language}

CREATE REPLIES FOR THESE CATEGORIES:

😊 **POSITIVE/PRAISE COMMENTS (4 replies):**
Example comments: "Great video!", "This was so helpful!", "Best channel ever!"
- Reply should: Thank them, encourage more engagement, ask a follow-up question

❓ **QUESTION COMMENTS (4 replies):**
Example comments: "How does this work?", "Can you explain more?", "What tool did you use?"
- Reply should: Answer helpfully, add value, encourage them to watch another video

😤 **CRITICAL/NEGATIVE COMMENTS (3 replies):**
Example comments: "This doesn't work", "You're wrong about this", "Waste of time"
- Reply should: Stay professional, address the concern, turn negativity into engagement

🔥 **ENGAGEMENT BOOSTING COMMENTS (3 replies):**
Example comments: "First!", "Who's watching in 2026?", Generic emoji comments
- Reply should: Create conversation, ask questions, boost algorithm signals

📌 **PINNED COMMENT SUGGESTION (1):**
Write the perfect pinned comment for this video that:
- Summarizes key value
- Asks an engaging question
- Encourages likes/subscriptions
- Under 3 lines

For each reply:
✅ Make it feel PERSONAL (not copy-paste)
✅ Include emoji naturally
✅ Keep under 2-3 sentences
✅ End with engagement trigger (question/CTA)`,

                summarizer: `You are an expert content analyst. Summarize this YouTube video transcript comprehensively.

Language for summary: ${language}

TRANSCRIPT:
${input}

PROVIDE:

📋 **QUICK SUMMARY (TL;DR):**
3-4 sentences capturing the entire video essence

🔑 **KEY POINTS (Main Takeaways):**
- List 5-7 most important points
- Each point in 1-2 sentences
- Include specific details/numbers mentioned

💡 **MAIN INSIGHT:**
The single most valuable takeaway from this video (1-2 sentences)

📊 **CONTENT BREAKDOWN:**
- Topic Category: [category]
- Content Type: [tutorial/review/opinion/news/etc.]
- Depth Level: [beginner/intermediate/advanced]

👥 **WHO SHOULD WATCH:**
1-2 sentences about who would benefit most from this video

✅ **ACTION ITEMS:**
3-5 specific things the viewer can do after watching

🔗 **RELATED TOPICS:**
5 related topics/videos the viewer might want to explore next

⭐ **CONTENT QUALITY ASSESSMENT:**
- Information Value: ⭐⭐⭐⭐⭐ (rate 1-5)
- Practical Usefulness: ⭐⭐⭐⭐⭐ (rate 1-5)
- Uniqueness: ⭐⭐⭐⭐⭐ (rate 1-5)`
            };
            return prompts[tool] || prompts.viral;
        }

        // YouTube Transcript
        async function fetchTranscript(videoId) {
            const proxyUrl = document.getElementById('transcriptProxy').value.trim();
            const videoUrl = `https://www.youtube.com/api/timedtext?lang=en&v=${videoId}`;
            
            try {
                const response = await fetch(proxyUrl ? `${proxyUrl}${encodeURIComponent(videoUrl)}` : videoUrl);
                if (!response.ok) throw new Error('Failed to fetch');
                const xmlText = await response.text();
                
                // Parse XML to extract text
                const parser = new DOMParser();
                const doc = parser.parseFromString(xmlText, 'text/xml');
                const textElements = doc.querySelectorAll('text');
                const texts = [];
                textElements.forEach(el => {
                    texts.push(el.textContent.trim());
                });
                
                return texts.join(' ');
            } catch (e) {
                console.error('Transcript fetch error:', e);
                return null;
            }
        }

        // Extract video ID
        function extractVideoId(url) {
            const patterns = [
                /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/|youtube\.com\/shorts\/)([0-9A-Za-z_-]{11})/,
                /^([0-9A-Za-z_-]{11})$/
            ];
            for (const pattern of patterns) {
                const match = url.match(pattern);
                if (match) return match[1];
            }
            return null;
        }

        // Main Generate Function
        async function generateContent() {
            const apiKey = document.getElementById('apiKey').value.trim();
            if (!apiKey) {
                showMessage('error', '⚠️ Please enter your Gemini API Key first!', '🔑 How to get your FREE API Key:<br><ol><li>Go to <a href="https://aistudio.google.com" target="_blank">aistudio.google.com</a></li><li>Sign in with your Google account</li><li>Click "Get API Key" → "Create API Key"</li><li>Copy the key and paste in sidebar</li></ol>');
                return;
            }

            let userContent = '';
            let videoTitle = 'Unknown';
            let videoAuthor = 'Unknown';

            if (currentTool === 'summarizer') {
                const url = document.getElementById('userUrl').value.trim();
                if (!url) {
                    showMessage('warning', '⚠️ Please enter a YouTube URL!');
                    return;
                }

                const videoId = extractVideoId(url);
                if (!videoId) {
                    showMessage('error', '❌ Invalid YouTube URL! Please use format: https://www.youtube.com/watch?v=xxxxx');
                    return;
                }

                showMessage('info', '📥 Downloading video transcript...');

                let transcript = await fetchTranscript(videoId);
                
                // Try to get video info
                try {
                    const proxyUrl = document.getElementById('transcriptProxy').value.trim();
                    const infoUrl = `https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=${videoId}&format=json`;
                    const infoResp = await fetch(proxyUrl ? `${proxyUrl}${encodeURIComponent(infoUrl)}` : infoUrl);
                    if (infoResp.ok) {
                        const info = await infoResp.json();
                        videoTitle = info.title;
                        videoAuthor = info.author_name;
                        showMessage('info', `📹 **Video:** ${videoTitle}<br>👤 **Channel:** ${videoAuthor}`);
                    }
                } catch(e) {}

                if (!transcript) {
                    showMessage('warning', '⚠️ Could not fetch transcript automatically. Please paste the transcript manually, or try a different video.', '💡 This video might not have subtitles/captions enabled, or CORS restrictions prevented access. Try adding a CORS proxy URL in the sidebar, or paste the transcript directly.');
                    
                    // Fallback: ask user to paste
                    const manualTranscript = prompt('Please paste the video transcript here:');
                    if (!manualTranscript) return;
                    transcript = manualTranscript;
                }

                userContent = `VIDEO TITLE: ${videoTitle}\nCHANNEL: ${videoAuthor}\n\n${transcript.substring(0, 5000)}`;
            } else {
                userContent = document.getElementById('userInput').value.trim();
                if (!userContent) {
                    showMessage('warning', '⚠️ Please enter a topic or keyword!');
                    return;
                }
            }

            // Start generation
            const btn = document.getElementById('generateBtn');
            btn.disabled = true;
            btn.classList.add('pulse');

            const progressContainer = document.getElementById('progressContainer');
            const progressFill = document.getElementById('progressFill');
            const progressText = document.getElementById('progressText');
            const resultsContainer = document.getElementById('resultsContainer');

            progressContainer.classList.add('active');
            resultsContainer.classList.remove('active');

            const progressMessages = [
                '🧠 Initializing SemTube AI Engine...',
                '🔍 Analyzing your request...',
                '📊 Processing with Gemini AI...',
                '✍️ Generating premium content...',
                '✨ Polishing the output...',
                '🎯 Almost there...'
            ];

            for (let i = 0; i < progressMessages.length; i++) {
                progressText.textContent = progressMessages[i];
                progressFill.style.width = `${(i + 1) * 16}%`;
                await new Promise(r => setTimeout(r, 600));
            }

            try {
                const { GoogleGenerativeAI } = window;
                const genAI = new GoogleGenerativeAI(apiKey);
                
                const modelNames = [
                    'gemini-2.0-flash',
                    'gemini-1.5-pro',
                    'gemini-1.5-flash',
                    'gemini-pro'
                ];

                let model = null;
                let modelName = '';

                for (const name of modelNames) {
                    try {
                        model = genAI.getGenerativeModel({ model: name });
                        modelName = name;
                        break;
                    } catch (e) {
                        continue;
                    }
                }

                if (!model) {
                    throw new Error('Could not initialize any Gemini model');
                }

                const tone = document.getElementById('tone').value;
                const language = document.getElementById('language').value;
                const audience = document.getElementById('audience').value;
                const length = document.getElementById('length').value;

                const prompt = getPrompt(currentTool, userContent, tone, language, audience, length);

                const result = await model.generateContent(prompt);
                const response = await result.response;
                generatedText = response.text();

                progressFill.style.width = '100%';
                progressFill.classList.add('active');
                await new Promise(r => setTimeout(r, 300));

                progressContainer.classList.remove('active');
                resultsContainer.classList.add('active');

                // Update results
                document.getElementById('resultBadge').innerHTML = `<span>${toolNames[currentTool]}</span>`;
                document.getElementById('resultBox').innerHTML = formatMarkdown(generatedText);
                document.getElementById('exportTextarea').value = generatedText;

                document.getElementById('resultsContainer').scrollIntoView({ behavior: 'smooth' });

            } catch (e) {
                progressContainer.classList.remove('active');
                
                const errMsg = e.message.toLowerCase();
                if (errMsg.includes('key') || errMsg.includes('api')) {
                    showMessage('error', '❌ API Key Issue:', '🔑 Make sure your API key is correct (no extra spaces)<br>• Try generating a new key from <a href="https://aistudio.google.com" target="_blank">aistudio.google.com</a><br>• Ensure you haven\'t exceeded the free quota');
                } else if (errMsg.includes('quota') || errMsg.includes('limit')) {
                    showMessage('warning', '⏳ Rate Limit Reached:', '• You\'ve made too many requests in a short time<br>• Wait 1-2 minutes and try again<br>• The free tier allows ~60 requests per minute');
                } else if (errMsg.includes('network') || errMsg.includes('fetch')) {
                    showMessage('error', '🌐 Connection Issue:', '• Check your internet connection<br>• Try refreshing the page<br>• If using VPN, try disabling it');
                } else {
                    showMessage('error', '❌ An error occurred:', `${e.message}<br><br>💡 Try refreshing the page and attempting again.`);
                }
            }

            btn.disabled = false;
            btn.classList.remove('pulse');
            progressFill.classList.remove('active');
        }

        // Format markdown-like text to HTML
        function formatMarkdown(text) {
            // Escape HTML
            let html = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
            
            // Headers
            html = html.replace(/^#### (.+)$/gm, '<h4>$1</h4>');
            html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
            html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
            html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');
            
            // Bold and Italic
            html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
            html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
            html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
            
            // Lists
            html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
            html = html.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');
            
            // Numbered lists
            html = html.replace(/^(\d+)\. (.+)$/gm, '<li>$2</li>');
            
            // Line breaks
            html = html.replace(/\n\n/g, '</p><p>');
            html = html.replace(/\n/g, '<br>');
            
            return `<p>${html}</p>`;
        }

        // Show message
        function showMessage(type, title, content = '') {
            // Remove existing messages
            const existingMsg = document.querySelector('.message-container');
            if (existingMsg) existingMsg.remove();

            const msgDiv = document.createElement('div');
            msgDiv.className = `message-box ${type} message-container`;
            msgDiv.innerHTML = `<h4>${title}</h4>${content ? `<p>${content}</p>` : ''}`;
            
            // Insert after input section
            const inputSection = document.querySelector('.input-section');
            inputSection.parentNode.insertBefore(msgDiv, inputSection.nextSibling);
            
            // Scroll to message
            msgDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
            
            // Auto remove after 10 seconds
            setTimeout(() => {
                msgDiv.style.opacity = '0';
                msgDiv.style.transform = 'translateX(-20px)';
                setTimeout(() => msgDiv.remove(), 300);
            }, 10000);
        }

        // Download functions
        function downloadTXT() {
            if (!generatedText) return;
            const blob = new Blob([generatedText], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `SemTube_${currentTool}.txt`;
            a.click();
            URL.revokeObjectURL(url);
        }

        function downloadMD() {
            if (!generatedText) return;
            const toolName = toolNames[currentTool];
            const content = `# SemTube AI Generated Content\n## Tool: ${toolName}\n\n---\n\n${generatedText}`;
            const blob = new Blob([content], { type: 'text/markdown' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `SemTube_${currentTool}.md`;
            a.click();
            URL.revokeObjectURL(url);
        }
    </script>
</body>
</html>
