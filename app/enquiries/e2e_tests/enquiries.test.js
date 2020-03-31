describe('Enquiries', () => {
  before(() => {
    cy.login('/enquiries/')
  })

  it('should render the header', () => {
    cy.contains('Ready to Trade')
  })

  it('should render the filters', () => {
    cy.get('.govuk-checkboxes__input').should('have.length', 9)
  })
})
