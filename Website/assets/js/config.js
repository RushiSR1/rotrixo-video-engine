/**
 * Rotrixo Global Configuration
 * Edit placeholders here to update links across all pages instantly.
 */
const ROTRIXO_CONFIG = {
  // Live demo Streamlit link
  STREAMLIT_DEMO_URL: 'https://rotrixo-video-engine-v21py.streamlit.app/',

  // Upwork Direct Contract Escrow checkout via email initiation
  UPWORK_URL: "mailto:hello@rotrixo.com?subject=I%27m%20interested%20and%20want%20my%20custom%20engine%20(%24199%20Beta%20Setup)&body=Hi%20Rushikesh%2C%0A%0AI%27m%20interested%20in%20deploying%20a%20custom%20autonomous%20video%20engine%20for%20my%20agency%20under%20the%20%24199%20Upwork%20Escrow%20beta%20deal.%0A%0APlease%20find%20my%20details%20below%20to%20generate%20the%20Upwork%20Direct%20Contract%20escrow%20link%3A%0A%0A1.%20My%20Name%3A%20%0A2.%20Agency%20%2F%20Brand%20Name%3A%20%0A3.%20Email%20for%20Upwork%20Direct%20Contract%20Generation%3A%20%0A4.%20Brief%20Overview%20of%20Our%20Business%20Needs%20%26%20Target%20Video%20Niche%3A%20%0A%0APlease%20send%20over%20the%20secure%20Upwork%20Escrow%20contract%20link.%0A%0AThank%20you!",

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

