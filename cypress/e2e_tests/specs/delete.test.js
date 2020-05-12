require('../support/commands')
const { results, details } = require('../selectors')

describe('Delete', () => {
  before(() => {
    cy.reseed('/enquiries/')
  })

  beforeEach(() => {
    Cypress.Cookies.preserveOnce('sessionid')
    Cypress.Cookies.preserveOnce('csrftoken')
  })

  context('when deleting an enquiry detail', () => {
    it('should check if you do wish to delete the enquiry', () => {
      cy.get(results.number(1)).contains('1Company')
      cy.get(results.number(1)).find('h3 a').click()
      cy.get(details.editDetailsButton).click()
      cy.get('main form > a').eq(1).click()
      cy.get('main div strong').contains(
        'Are you sure you want to delete this enquiry?'
      )
      cy.get('main form button').contains('Delete enquiry')
      cy.get('main form button').click()
    })
    it('should not appear in the results', () => {
      cy.get(results.number(1)).contains('ABC Electronics Co.')
    })
  })
})
