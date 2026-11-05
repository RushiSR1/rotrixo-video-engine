/**
 * Rotrixo Global Configuration
 * Edit placeholders here to update links across all pages instantly.
 */
const ROTRIXO_CONFIG = {
  // Live demo Streamlit link
  STREAMLIT_DEMO_URL: 'https://YOUR-STREAMLIT-APP-URL.streamlit.app',

  // Upwork Direct Contract or Profile URL for escrow checkout
  UPWORK_URL: 'https://www.upwork.com/YOUR-PROFILE-OR-CONTRACT-LINK',

  // Primary business inquiry email
  EMAIL: 'hello@rotrixo.com',

  // Canonical base domain
  SITE_URL: 'https://rotrixo.com',

  // Founder profile details
  FOUNDER_NAME: 'Rushikesh Rautrao',
  FOUNDER_ROLE: 'Founder & AI Automation Engineer',

  // Beta spots remaining (dynamic display)
  BETA_SPOTS_TOTAL: 2,
  BETA_SPOTS_REMAINING: 2,

  // Social / Community placeholders
  SOCIAL: {
    TWITTER: 'https://twitter.com/rotrixo',
    LINKEDIN: 'https://linkedin.com/in/rushikesh-rautrao',
    GITHUB: 'https://github.com/rotrixo'
  }
};

// Expose globally for vanilla JS without bundling
if (typeof window !== 'undefined') {
  window.ROTRIXO_CONFIG = ROTRIXO_CONFIG;
}

// Export for module support if loaded in modular context
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ROTRIXO_CONFIG;
}

