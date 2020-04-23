require('../support/commands')
const { assertSummaryList } = require('../support/assertions')
const { results, details } = require('../selectors')

describe('Edit', () => {
  before(() => {
    cy.login('/enquiries/')
    Cypress.Cookies.preserveOnce('sessionid')
  })

  context('when viewing the enquiry details', () => {
    it('should render the details', () => {
      cy.get(results.number(1)).find('h3 a').click()

      cy.get(details.topControls)
        .find('a')
        .eq(0)
        .should('have.text', 'Back')
        .and('have.attr', 'href', '/enquiries/')
        .parents()
        .find('button')
        .should('contain', 'Edit details')

      cy.get('main')
        .find('div')
        .find('h2')
        .should('have.text', '1Company')
        .next()
        .then($element =>
          assertSummaryList($element, [
            { dt: 'Date received', dd: '21 February 2020' },
            {
              dt: 'Date last updated',
              dd: '25 February 2020',
            },
            {
              dt: 'Enquiry stage',
              dd: 'Awaiting response from Investor',
            },
            { dt: 'Owner', dd: 'IST User 5' },
            { dt: 'Company in Data Hub', dd: '----' },
          ])
        )

      cy.findDetailsSection(1)
        .should('have.text', 'Enquiry details')
        .next()
        .then($element =>
          assertSummaryList($element, [
            { dt: 'Enquiry text', dd: 'Internet startup company' },
            {
              dt: 'Investment readiness',
              dd: 'I’m convinced and want to talk to someone about my plans',
            },
            { dt: 'Enquiry quality', dd: 'FDI or likely FDI' },
            { dt: 'First response channel', dd: 'Email' },
          ])
        )

      cy.findDetailsSection(2)
        .should('have.text', 'Company details')
        .next()
        .then($element =>
          assertSummaryList($element, [
            { dt: 'Website', dd: 'https://www.example.com/' },
            {
              dt: 'Country',
              dd: 'Saudi Arabia',
            },
            { dt: 'Region', dd: 'EMEA' },
            {
              dt: 'Company HQ address',
              dd:
                'ABC Electronics Co. (UK), Infinity Park Derby, Sinfin Moor Ln, Derby, DE24 9QG, United Kingdom',
            },
            { dt: 'Primary sector', dd: 'Advanced Engineering' },
            { dt: 'IST sector', dd: 'ITECH' },
          ])
        )

      cy.findDetailsSection(3)
        .should('have.text', 'Contact details')
        .next()
        .then($element =>
          assertSummaryList($element, [
            { dt: 'First name', dd: 'Jeff' },
            {
              dt: 'Last name',
              dd: 'Bezo',
            },
            { dt: 'Job title', dd: 'Editor' },
            {
              dt: 'Email',
              dd: 'jeff.bezos@washingtonpost.com',
            },
            { dt: 'Phone', dd: '+1 202 334 6000' },
            { dt: 'Call requested', dd: 'Yes - afternoon' },
          ])
        )

      cy.findDetailsSection(4)
        .should('have.text', 'Marketing information')
        .next()
        .then($element =>
          assertSummaryList($element, [
            { dt: 'Google campaign', dd: '#r.4142563726849_345374257' },
            {
              dt: 'Marketing channel',
              dd: 'IiGB',
            },
            { dt: 'How did they hear about DIT?', dd: 'Internet search' },
            {
              dt: 'Consent (email)',
              dd: 'No',
            },
            { dt: 'Consent (telephone)', dd: 'No' },
          ])
        )

      cy.findDetailsSection(5)
        .should('have.text', 'HPO details')
        .next()
        .then($element =>
          assertSummaryList($element, [
            { dt: 'First HPO selection', dd: '----' },
            {
              dt: 'Second HPO selection',
              dd: '----',
            },
            { dt: 'Third HPO selection', dd: '----' },
          ])
        )

      cy.findDetailsSection(6)
        .should('have.text', 'Data Hub details')
        .next()
        .then($element =>
          assertSummaryList($element, [
            { dt: 'Organisation type', dd: 'Limited company' },
            {
              dt: 'Investment type',
              dd: 'Expansion of existing site or activity',
            },
            { dt: 'Project name', dd: 'ABC Hummingbird' },
            {
              dt: 'Project description',
              dd: 'Expansion of ABC Hummingbird factory sites',
            },
            {
              dt: 'Anonymised project description',
              dd: 'Expansion of factory sites',
            },
            { dt: 'Estimated land date', dd: '03 February 2021' },
            { dt: 'New or existing investor', dd: 'EXISTING,' },
            { dt: 'Investor level of involvement', dd: 'FDI Hub + Post' },
            {
              dt: 'Specific investment programme',
              dd: 'Invest in Great Britain',
            },
            { dt: 'CRM', dd: 'Data Hub user 1' },
            { dt: 'Date added to Data Hub', dd: '03 February 2020' },
            { dt: 'Project code', dd: '42901' },
            { dt: 'Data Hub project status', dd: 'Active' },
            { dt: 'Project success date', dd: '03 February 2022' },
          ])
        )

      cy.findDetailsSection(7)
        .should('have.text', 'Notes')
        .next()
        .then($element =>
          assertSummaryList($element, [
            {
              dt: 'Notes',
              dd:
                'This is the notes section. The IST user can add any notes relating to the enquiry. This is a textarea and the user can input multiple lines of text.',
            },
          ])
        )
    })
  })
})
