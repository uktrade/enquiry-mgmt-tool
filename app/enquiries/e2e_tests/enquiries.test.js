describe('Enquiries Summary view', () => {
  before(() => {
    cy.login('/enquiries/')
  })

  it('should render the header', () => {
    cy.contains('Ready to Trade')
  })
})
