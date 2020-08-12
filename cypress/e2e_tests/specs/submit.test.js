require('../support/commands')
const { results, details } = require('../selectors')

const getTestCompany = (name) => {
  cy.contains('label', 'Company name')
    .parent()
    .find('input')
    .clear()
    .type(name)
  
  cy.contains('Apply filters')
    .click()

  cy.get(results.number(1)).find('h3 a').click()
}

const getDetail = field => 
  cy.get('dt')
    .contains(field)
    .parent()
    .find('dd')

// In the absence of integration testing with DH, this tests logic around the visibility of the 'Submit' button
describe('Submit', () => {

  beforeEach(() => {
    cy.reseed('/enquiries/')
    Cypress.Cookies.preserveOnce('sessionid')
  })

  context('when viewing an enquiry with an added to DH status', () => {
    it('should not display the option to submit an enquiry to DataHub', () => {
      getTestCompany('DH ENQUIRY STAGE')

      getDetail('Date added to Data Hub').should('contain', 'Date not recorded')
      getDetail('Enquiry stage').should('contain', 'Added to Data Hub')

      cy.get(details.submit).should('not.exist');

    })
  })

  context('when viewing an enquiry with an added to DH date', () => {
    it('should not display the option to submit an enquiry to DataHub', () => {
      getTestCompany('NEW WITH DH DATE')

      getDetail('Date added to Data Hub').should('contain', '03 February 2020')
      getDetail('Enquiry stage').should('not.contain', 'Added to Data Hub')

      cy.get(details.submit).should('not.exist');

    })
  })

  context('when viewing without either a DH added status or date', () => {
    it('should display the option to submit an enquiry to DataHub', () => {
      getTestCompany('NO DH INFO')

      getDetail('Date added to Data Hub').should(
        'contain',
        'Enquiry not added to Data Hub'
      )
      getDetail('Enquiry stage').should('not.contain', 'Added to Data Hub')

      cy.get(details.submit).should('exist');
    })
  })
})
