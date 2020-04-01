describe('Enquiries Summary view', () => {
  before(() => {
    cy.visit('/enquiries/')
  })

  it('should render the header', () => {
    cy.contains('Ready to Trade')
  })

  it('should render the filters', () => {
    cy.get('.govuk-checkboxes__input').should('have.length', 8)
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
    cy.visit('/enquiries/')
    cy.viewEnquiry(2)
  })

  it('should render the header and back link', () => {
    cy.contains('Ready to Trade')
    cy.get('.govuk-back-link').should('have.length', 1)
  })

  it('should have one large heading with expectd name', () => {
    cy.get('.govuk-heading-l').should('have.length', 1)
    cy.contains('MATCHBOX LTD')
  })
})


describe('Enquiry edit company name', () => {
  before(() => {
    cy.viewEnquiry(2)
  })

  it('should update company name using edit button', () => {
    cy.contains('Edit details').click()
    cy.get('input[name=company_name]').clear().type('Matchbox Corp')
    cy.contains('Save and return').click()
  })

  it('should have updated company name', () => {
    cy.get('.govuk-heading-l').should('have.length', 1)
    cy.contains('Matchbox Corp')
  })
})
