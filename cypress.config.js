const { defineConfig } = require('cypress')

module.exports = defineConfig({
  video: false,
  videoUploadOnPasses: false,
  screenshotOnRunFailure: false,
  defaultCommandTimeout: 10000,
  e2e: {
    setupNodeEvents(on, config) {},
    specPattern: 'cypress/e2e_tests/specs//**/*.cy.{js,jsx,ts,tsx}',
    baseUrl: 'http://localhost:8001',
  },
})
