const { pagination, results } = require('../selectors')

describe('Pagination', () => {
  before(() => {
    cy.login('/enquiries/')
    Cypress.Cookies.preserveOnce('sessionid')
  })

  it('should page to the previous page', () => {
    cy.get(pagination.pageLink(1)).should('have.text', '1')
    cy.get(pagination.lastPageLink).should('have.text', 'Next')
    cy.get(pagination.headerPageNumber).should('have.text', 'Page 1 of 4')
    cy.get(pagination.pageLink(2)).click()
    cy.get(pagination.headerPageNumber).should('have.text', 'Page 2 of 4')
    cy.get(pagination.pageLink(1)).should('have.text', 'Previous')
    cy.get(pagination.pageLink(1)).click()
    cy.get(pagination.headerPageNumber).should('have.text', 'Page 1 of 4')
    cy.get(pagination.pageLink(1)).should('have.text', '1')
  })

  it('should update the enquiries', () => {
    cy.get(results.number(1)).find('h3 a').should('have.text', '1Company')
    cy.get(pagination.pageLink(2)).click()
    cy.get(results.number(1))
      .find('h3 a')
      .should('have.text', 'Alphabet Projects')
  })
})
