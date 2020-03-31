describe('Enquiries Summary view', () => {
  before(() => {
    cy.login('/enquiries/')
  })

  it('should render the header', () => {
    cy.contains('Ready to Trade')
  })

  it('should render the filters', () => {
    cy.get('.govuk-checkboxes__input').should('have.length', 14)
  })

  it('should render enquiries count', () => {
    cy.get('.big-number-of-enquiries').should('have.length', 1)
  })

  it('should have 10 enquiry titles in each page', () => {
    cy.get('.entity-title-link').should('have.length', 10)
  })

  it('should have 10 enquiry badges list in each page', () => {
    cy.get('.entity-badges-list').should('have.length', 10)
  })
})


describe('Enquiry Detail view', () => {
  before(() => {
    // cy.login('/enquiries/')
    cy.viewEnquiry(2)
  })

  it('should render the header', () => {
    cy.contains('Ready to Trade')
  })

  it('should have one back link to summary page', () => {
    cy.get('.govuk-back-link').should('have.length', 1)
  })

  it('should have one large heading', () => {
    cy.get('.govuk-heading-l').should('have.length', 1)
  })

  it('should have correct company name', () => {
    cy.contains('MATCHBOX LTD')
  })
})


describe('Enquiry edit view', () => {
  before(() => {
    cy.login('/enquiries/')
    cy.editEnquiry(2)
  })

  it('should render the header', () => {
    cy.contains('Ready to Trade')
  })

  it('should have one back link to summary page', () => {
    cy.get('.govuk-back-link').should('have.length', 1)
  })

  it('should have one large heading with expected value for this id', () => {
    cy.get('.govuk-heading-l').should('have.length', 1)
    cy.contains('MATCHBOX LTD')
  })

  it('should update company name', () => {
    cy.get('input[name=company_name]').type('Matchbox Corp')
    cy.contains('Save and return').click()
  })
})
