describe('Enquiries', () => {
  before(() => {
    cy.visit('/enquiries/')
  })

  it('should render the header', () => {
    cy.contains('Ready to Trade')
  })
})
