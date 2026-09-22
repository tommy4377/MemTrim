import { mount } from 'svelte'
import App from './App.svelte'
// Import themes first, then tokens (tokens has base variables, themes override them)
import './theme/tokens.css'
import './theme/common.css'

const target = document.getElementById('app')
if (!target) {
  throw new Error('MemTrim root element #app was not found')
}

const app = mount(App, { target })

// Disable the default WebView2 context menu (Refresh, Save as, Share, ...)
// only in production; in dev it stays available for Inspect Element
if (import.meta.env.PROD) {
  document.addEventListener('contextmenu', (e) => e.preventDefault())
}

// Disable dev tools shortcuts only in production
if (import.meta.env.PROD) {
  document.addEventListener('keydown', (e) => {
    if (
      e.key === 'F12' ||
      (e.ctrlKey && e.shiftKey && e.key === 'I') ||
      (e.ctrlKey && e.shiftKey && e.key === 'C') ||
      (e.ctrlKey && e.shiftKey && e.key === 'J') ||
      (e.ctrlKey && e.key === 'u')
    ) {
      e.preventDefault()
      return false
    }
    return true
  })
}

// Remove the loading state once the app has mounted
setTimeout(() => {
  document.getElementById('app')?.classList.add('loaded')
}, 100)

export default app
