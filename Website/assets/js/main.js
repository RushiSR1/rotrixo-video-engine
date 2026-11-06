/**
 * ROTRIXO MAIN JAVASCRIPT
 * Handles navigation, mobile drawer, animations, terminal simulator,
 * FAQ accordion, Netlify forms, and dynamic configuration bindings.
 */

function initAll() {
  initDynamicConfig();
  initNavbar();
  initMobileMenu();
  initActiveNavLink();
  initScrollReveal();
  initWorkflowTerminal();
  initFaqAccordion();
  initContactForm();
  initFooterYear();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initAll);
} else {
  initAll();
}

/**
 * 1. Dynamic Config Links & Texts
 */
function initDynamicConfig() {
  const config = window.ROTRIXO_CONFIG;
  if (!config) return;

  // Update hrefs
  document.querySelectorAll('[data-config-link]').forEach(el => {
    const key = el.getAttribute('data-config-link');
    if (key === 'EMAIL') {
      el.href = `mailto:${config.EMAIL}`;
    } else if (config[key]) {
      el.href = config[key];
    }
  });

  // Update text contents
  document.querySelectorAll('[data-config-text]').forEach(el => {
    const key = el.getAttribute('data-config-text');
    if (config[key]) {
      el.textContent = config[key];
    }
  });

  // Beta spots indicator
  const spotsEl = document.querySelector('[data-beta-spots]');
  if (spotsEl) {
    spotsEl.textContent = `${config.BETA_SPOTS_REMAINING} / ${config.BETA_SPOTS_TOTAL}`;
  }
}

/**
 * 2. Sticky Navbar Blur & Shadow on Scroll
 */
function initNavbar() {
  const navbar = document.getElementById('main-navbar');
  if (!navbar) return;

  const onScroll = () => {
    if (window.scrollY > 20) {
      navbar.classList.add('bg-[#05060A]/90', 'backdrop-blur-md', 'border-b', 'border-white/10', 'shadow-2xl');
      navbar.classList.remove('bg-transparent');
    } else {
      navbar.classList.remove('shadow-2xl');
    }
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

/**
 * 3. Mobile Navigation Drawer
 */
window.toggleRotrixoMobileMenu = function() {
  const toggleBtn = document.getElementById('mobile-menu-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  const menuIcon = document.getElementById('menu-icon');
  const closeIcon = document.getElementById('close-icon');

  if (!mobileMenu) return;

  const isHidden = mobileMenu.classList.contains('hidden') || 
                   mobileMenu.style.display === 'none' || 
                   (window.getComputedStyle && window.getComputedStyle(mobileMenu).display === 'none');
  
  if (isHidden) {
    // Open
    mobileMenu.classList.remove('hidden');
    mobileMenu.style.display = 'block';
    if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'true');
    if (menuIcon) menuIcon.classList.add('hidden');
    if (closeIcon) closeIcon.classList.remove('hidden');
  } else {
    // Close
    mobileMenu.classList.add('hidden');
    mobileMenu.style.display = 'none';
    if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'false');
    if (menuIcon) menuIcon.classList.remove('hidden');
    if (closeIcon) closeIcon.classList.add('hidden');
  }
};

function initMobileMenu() {
  const toggleBtn = document.getElementById('mobile-menu-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  const menuIcon = document.getElementById('menu-icon');
  const closeIcon = document.getElementById('close-icon');

  if (!mobileMenu) return;

  if (toggleBtn) {
    toggleBtn.removeEventListener('click', window.toggleRotrixoMobileMenu);
    toggleBtn.addEventListener('click', window.toggleRotrixoMobileMenu);
  }

  // Close when clicking mobile links
  mobileMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      mobileMenu.classList.add('hidden');
      mobileMenu.style.display = 'none';
      if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'false');
      if (menuIcon) menuIcon.classList.remove('hidden');
      if (closeIcon) closeIcon.classList.add('hidden');
      document.body.style.overflow = '';
    });
  });

  // Close on Escape
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !mobileMenu.classList.contains('hidden')) {
      window.toggleRotrixoMobileMenu();
    }
  });
}

/**
 * 4. Active Nav Link Highlighting
 */
function initActiveNavLink() {
  const currentPath = window.location.pathname.replace(/\/$/, '') || '/';
  const navLinks = document.querySelectorAll('.nav-link, .mobile-nav-link');
  const bottomLinks = document.querySelectorAll('.mobile-bottom-link');

  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (!href) return;
    const cleanHref = href.replace(/\/$/, '').replace(/\.html$/, '') || '/';

    // Exact match or clean match
    if (
      (currentPath === '/' && (cleanHref === '/' || cleanHref === '/index')) ||
      (currentPath !== '/' && (currentPath === cleanHref || currentPath === `${cleanHref}.html`))
    ) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });

  bottomLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (!href) return;
    const cleanHref = href.replace(/\/$/, '').replace(/\.html$/, '') || '/';

    if (
      (currentPath === '/' && (cleanHref === '/' || cleanHref === '/index')) ||
      (currentPath !== '/' && (currentPath === cleanHref || currentPath === `${cleanHref}.html`))
    ) {
      link.classList.add('text-emerald-400');
      link.classList.remove('text-slate-400');
    }
  });
}

/**
 * 5. Scroll Reveal with IntersectionObserver
 */
function initScrollReveal() {
  const reveals = document.querySelectorAll('.reveal');
  if (!reveals.length) return;

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('active');
          obs.unobserve(entry.target);
        }
      });
    }, {
      root: null,
      rootMargin: '0px 0px -40px 0px',
      threshold: 0.15
    });

    reveals.forEach(el => observer.observe(el));
  } else {
    // Fallback if observer not supported
    reveals.forEach(el => el.classList.add('active'));
  }
}

/**
 * 6. Hero Workflow Terminal Simulator
 */
function initWorkflowTerminal() {
  const terminal = document.getElementById('workflow-terminal');
  if (!terminal) return;

  const timerEl = document.getElementById('terminal-timer');
  const progressBar = document.getElementById('terminal-progress');
  const logEl = document.getElementById('terminal-live-log');
  const stepItems = terminal.querySelectorAll('[data-workflow-step]');

  const steps = [
    { title: 'Benchmarking Viral Hooks', log: '[APIFY] Scraping top 100 trending shorts in niche... Found 8 high-retention patterns (Hook retention > 84%).' },
    { title: 'Generating AI Script', log: '[GEMINI] Synthesizing 42s script with psychological curiosity loop and 3 visual scene beats.' },
    { title: 'Synthesizing Neural Voice', log: '[ELEVENLABS] Generating ultra-realistic human cadence via neural model (en-US, 48kHz WAV).' },
    { title: 'Matching Stock Footage', log: '[PIXABAY] Sourcing 4 vertical 1080x1920 clips; aligning transitions to speech syllable peaks.' },
    { title: 'Exporting High-Retention MP4', log: '[FFMPEG] Merging audio, clips & kinetic word-by-word subtitles. Output saved: 1080x1920 60FPS MP4.' }
  ];

  let currentStep = 0;
  let seconds = 0;
  let timerInterval = null;
  let stepInterval = null;

  function runCycle() {
    currentStep = 0;
    seconds = 0;
    if (progressBar) progressBar.style.width = '0%';
    
    // Reset step UI
    stepItems.forEach(item => {
      const badge = item.querySelector('.step-status-badge');
      const icon = item.querySelector('.step-check-icon');
      if (badge) badge.className = 'step-status-badge px-2 py-0.5 rounded text-xs font-mono text-slate-400 bg-white/5';
      if (badge) badge.textContent = 'QUEUED';
      if (icon) icon.classList.add('opacity-20');
      item.classList.remove('border-emerald-500/50', 'bg-white/5');
    });

    // Start timer counter
    clearInterval(timerInterval);
    timerInterval = setInterval(() => {
      seconds += 1;
      const formatted = `00:${seconds < 10 ? '0' : ''}${seconds}s`;
      if (timerEl) timerEl.textContent = formatted;
      if (seconds >= 58) {
        clearInterval(timerInterval);
      }
    }, 1000);

    function advanceStep() {
      if (currentStep >= steps.length) {
        // Complete cycle pause, then restart
        if (logEl) logEl.textContent = '[SUCCESS] Ready for upload! Pipeline cycle completed in 58 seconds.';
        if (progressBar) progressBar.style.width = '100%';
        setTimeout(runCycle, 4000);
        return;
      }

      const activeStepData = steps[currentStep];
      const targetItem = stepItems[currentStep];

      if (targetItem) {
        const badge = targetItem.querySelector('.step-status-badge');
        const icon = targetItem.querySelector('.step-check-icon');
        if (badge) {
          badge.className = 'step-status-badge px-2 py-0.5 rounded text-xs font-mono text-emerald-400 bg-emerald-500/10 border border-emerald-500/20';
          badge.textContent = 'DONE ✓';
        }
        if (icon) {
          icon.classList.remove('opacity-20');
          icon.classList.add('text-emerald-400');
        }
        targetItem.classList.add('border-emerald-500/30', 'bg-emerald-500/5');
      }

      if (logEl) {
        logEl.textContent = activeStepData.log;
      }

      if (progressBar) {
        const pct = Math.round(((currentStep + 1) / steps.length) * 100);
        progressBar.style.width = `${pct}%`;
      }

      currentStep++;
      setTimeout(advanceStep, 2200);
    }

    advanceStep();
  }

  runCycle();
}

/**
 * 7. FAQ Accordion Handler
 */
function initFaqAccordion() {
  const faqButtons = document.querySelectorAll('.faq-toggle-btn');
  if (!faqButtons.length) return;

  faqButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const expanded = btn.getAttribute('aria-expanded') === 'true';
      const targetId = btn.getAttribute('aria-controls');
      const answerEl = document.getElementById(targetId);
      const icon = btn.querySelector('.faq-icon');

      // Close other accordions in the same group
      faqButtons.forEach(otherBtn => {
        if (otherBtn !== btn) {
          otherBtn.setAttribute('aria-expanded', 'false');
          const otherTargetId = otherBtn.getAttribute('aria-controls');
          const otherAnswer = document.getElementById(otherTargetId);
          const otherIcon = otherBtn.querySelector('.faq-icon');
          if (otherAnswer) otherAnswer.classList.add('hidden');
          if (otherIcon) otherIcon.style.transform = 'rotate(0deg)';
        }
      });

      if (expanded) {
        btn.setAttribute('aria-expanded', 'false');
        if (answerEl) answerEl.classList.add('hidden');
        if (icon) icon.style.transform = 'rotate(0deg)';
      } else {
        btn.setAttribute('aria-expanded', 'true');
        if (answerEl) answerEl.classList.remove('hidden');
        if (icon) icon.style.transform = 'rotate(180deg)';
      }
    });
  });
}

/**
 * 8. Netlify Contact Form AJAX Handler
 */
function initContactForm() {
  const form = document.querySelector('form[name="contact"]');
  if (!form) return;

  const submitBtn = form.querySelector('button[type="submit"]');
  const statusContainer = document.getElementById('form-status-message');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    const formData = new FormData(form);
    const originalBtnText = submitBtn ? submitBtn.innerHTML : 'Submit';

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = `
        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
        </svg>
        Transmitting Specifications...
      `;
    }

    try {
      const response = await fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(formData).toString()
      });

      if (response.ok || response.status === 200 || response.type === 'opaque') {
        form.reset();
        if (statusContainer) {
          statusContainer.className = 'mt-6 p-5 rounded-xl border border-emerald-500/40 bg-emerald-500/10 text-emerald-300 flex items-start gap-3';
          statusContainer.innerHTML = `
            <svg class="w-6 h-6 text-emerald-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <h4 class="font-bold text-white text-base">Transmission Successfully Received</h4>
              <p class="text-sm text-slate-300 mt-1">Thank you for submitting your workflow requirements. Rushikesh will review your agency details and reply within 4 hours to confirm your custom setup scope.</p>
            </div>
          `;
          statusContainer.classList.remove('hidden');
        }
      } else {
        throw new Error('Network response was not ok.');
      }
    } catch (err) {
      console.warn('Netlify form submission fallback:', err);
      if (statusContainer) {
        statusContainer.className = 'mt-6 p-5 rounded-xl border border-amber-500/40 bg-amber-500/10 text-amber-300 flex items-start gap-3';
        statusContainer.innerHTML = `
          <svg class="w-6 h-6 text-amber-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <div>
            <h4 class="font-bold text-white text-base">Notice: Direct Dispatch Available</h4>
            <p class="text-sm text-slate-300 mt-1">If the submission was interrupted, you can email Rushikesh directly at <a href="mailto:hello@rotrixo.com" class="underline text-emerald-400">hello@rotrixo.com</a> with your agency name and specs.</p>
          </div>
        `;
        statusContainer.classList.remove('hidden');
      }
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
      }
    }
  });
}

/**
 * 9. Auto Footer Year
 */
function initFooterYear() {
  const yearEls = document.querySelectorAll('.current-year');
  const year = new Date().getFullYear();
  yearEls.forEach(el => {
    el.textContent = year.toString();
  });
}

