require('../support/commands')

const searchByCompanyName = company =>
  cy.contains('label', 'Company name').parent().find('input').type(company)

const truncatedEnquiryText =
  'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure...'

const shorterEnquiryText =
  'Matchbox are looking to expand our presence in the UK by opening a new central London office to complement our existing UK office in Edinburgh. We have secured a site in west London and are looking for more.'

describe('View list of enquiries', () => {
  context('Enquiry text', () => {
    beforeEach(() => {
      cy.reseed('/enquiries/')
      Cypress.Cookies.preserveOnce('sessionid')
    })
    it('Should truncate enquiry text if more than 250 characters but keep final word intact', () => {
      searchByCompanyName('long text')
      cy.contains('Apply filters').click()
      cy.contains('Enquiry text')
        .next()
        .should('have.text', truncatedEnquiryText)
    })
    it('Should not truncate enquiry text if less than 250 characters', () => {
      searchByCompanyName('shorter text')
      cy.contains('Apply filters').click()
      cy.contains('Enquiry text')
        .next()
        .should('have.text', shorterEnquiryText)
    })
  })
})
