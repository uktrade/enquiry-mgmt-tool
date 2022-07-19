const { format } = require('date-fns')
require('../support/commands')
const {
  assertSummaryDetails,
  assertEnquiryForm,
  NOT_EDITABLE,
} = require('../support/assertions')
const { results, details } = require('../selectors')

describe('Edit', () => {
  before(() => {
    cy.reseed('/')
  })

  beforeEach(() => {
    Cypress.Cookies.preserveOnce('sessionid')
    Cypress.Cookies.preserveOnce('csrftoken')
  })

  context('when viewing the enquiry details', () => {
    it('should render the details', () => {
      cy.get(results.number(1)).find('h3 a').click()
      cy.get(details.topControls)
        .find('a')
        .eq(0)
        .should('have.text', 'Back')
        .and('have.attr', 'href', '/')
        .parents()
        .find('a')
        .should('contain', 'Edit details')

      assertSummaryDetails([
        {
          title: '1Company',
          summaryList: [
            { dt: 'Date received', dd: '21 February 2020' },
            {
              dt: 'Date last updated',
              dd: '25 February 2020',
            },
            {
              dt: 'Enquiry stage',
              dd: 'Awaiting response from Investor',
            },
            { dt: 'Owner', dd: 'Aiden Collet' },
            { dt: 'Company in Data Hub', dd: '----' },
          ],
        },
        {
          title: 'Enquiry details',
          summaryList: [
            { dt: 'Enquiry text', dd: 'Internet startup company' },
            {
              dt: 'Investment readiness',
              dd: 'I’m convinced and want to talk to someone about my plans',
            },
            { dt: 'Enquiry quality', dd: 'FDI or likely FDI' },
            { dt: 'First response channel', dd: 'Email' },
          ],
        },
        {
          title: 'Company details',
          summaryList: [
            { dt: 'Website', dd: 'https://www.example.com/' },
            {
              dt: 'Country',
              dd: 'Saudi Arabia',
            },
            { dt: 'Region', dd: 'EMEA' },
            {
              dt: 'Company HQ address',
              dd: 'ABC Electronics Co. (UK), Far Far Away, United Kingdom',
            },
            { dt: 'Primary sector', dd: 'Advanced engineering' },
            { dt: 'IST sector', dd: 'ITECH' },
          ],
        },
        {
          title: 'Contact details',
          summaryList: [
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
          ],
        },
        {
          title: 'Marketing information',
          summaryList: [
            { dt: 'Google campaign', dd: '#r.4142563726849_345374257' },
            {
              dt: 'Marketing channel',
              dd: 'Website',
            },
            { dt: 'How did they hear about DIT?', dd: 'Internet search' },
            {
              dt: 'Consent (email)',
              dd: 'Maybe',
            },
            { dt: 'Consent (telephone)', dd: 'Maybe' },
          ],
        },
        {
          title: 'HPO details',
          summaryList: [
            { dt: 'First HPO selection', dd: '----' },
            {
              dt: 'Second HPO selection',
              dd: '----',
            },
            { dt: 'Third HPO selection', dd: '----' },
          ],
        },
        {
          title: 'Data Hub details',
          summaryList: [
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
              dd: 'Invest in GREAT Britain',
            },
            { dt: 'Client Relationship Manager', dd: 'Data Hub user 1' },
            { dt: 'Date added to Data Hub', dd: '03 February 2020' },
            { dt: 'Project code', dd: 'DHP-00000001' },
            { dt: 'Project success date', dd: '03 February 2022' },
          ],
        },
        {
          title: 'Notes',
          summaryList: [
            {
              dt: 'Notes',
              dd:
                'This is the notes section. The IST user can add any notes relating to the enquiry. This is a textarea and the user can input multiple lines of text.',
            },
          ],
        },
      ])
    })
  })

  context('when editing the enquiry', () => {
    it('should render the form', () => {
      cy.get(details.editDetailsButton).click()
      assertEnquiryForm([
        {
          title: 'Enquiry overview',
          formFields: [
            {
              type: 'text',
              label: 'Company name',
              value: '1Company',
            },
            {
              type: 'text',
              label: 'Company HQ address',
              value: 'ABC Electronics Co. (UK), Far Far Away, United Kingdom',
            },
            {
              type: 'select',
              label: 'Enquiry stage',
              value: 'AWAITING_RESPONSE',
            },
            {
              type: 'select',
              label: 'Owner',
              value: '5',
            },
            {
              type: 'address',
              label: 'Company in Data Hub',
              address: 'None',
            },
          ],
        },
        {
          title: 'Enquiry details',
          formFields: [
            {
              type: NOT_EDITABLE,
              label: 'Enquiry text',
              value: 'Internet startup company',
            },
            {
              type: 'select',
              label: 'Investment readiness',
              value: 'CONVINCED',
            },
            {
              type: 'select',
              label: 'Enquiry quality',
              value: 'LIKELY_FDI',
            },
            {
              type: 'select',
              label: 'First response channel',
              value: 'EMAIL',
            },
          ],
        },
        {
          title: 'Company details',
          formFields: [
            {
              type: 'text',
              label: 'Website',
              value: 'https://www.example.com/',
            },
            {
              type: 'select',
              label: 'Country',
              value: 'SA',
            },
            {
              type: 'select',
              label: 'Region',
              value: 'EMEA',
            },
            {
              type: 'select',
              label: 'Primary sector',
              value: 'ADVANCED_ENG',
            },
            {
              type: 'select',
              label: 'IST sector',
              value: 'ITECH',
            },
          ],
        },
        {
          title: 'Contact',
          formFields: [
            {
              type: 'text',
              label: 'First name',
              value: 'Jeff',
            },
            {
              type: 'text',
              label: 'Last name',
              value: 'Bezo',
            },
            {
              type: 'text',
              label: 'Job title',
              value: 'Editor',
            },
            {
              type: 'text',
              label: 'Email',
              value: 'jeff.bezos@washingtonpost.com',
            },
            {
              type: 'text',
              label: 'Telephone country code',
              value: 'None',
            },
            {
              type: 'text',
              label: 'Phone',
              value: '+1 202 334 6000',
            },
            {
              type: 'select',
              label: 'Call requested',
              value: 'YES_AFTERNOON',
            },
          ],
        },
        {
          title: 'Marketing',
          formFields: [
            {
              type: 'text',
              label: 'Google campaign',
              value: '#r.4142563726849_345374257',
            },
            {
              type: 'select',
              label: 'Marketing channel',
              value: 'IIGB',
            },
            {
              type: 'select',
              label: 'How did they hear about DIT?',
              value: 'INTERNET_SEARCH',
            },
            {
              type: 'select',
              label: 'Consent (email)',
              value: 'False',
            },
            {
              type: 'select',
              label: 'Consent (telephone)',
              value: 'False',
            },
          ],
        },
        {
          title: 'HPO details',
          formFields: [
            {
              type: 'select',
              label: 'First HPO selection',
              value: 'DEFAULT',
            },
            {
              type: 'select',
              label: 'Second HPO selection',
              value: 'DEFAULT',
            },
            {
              type: 'select',
              label: 'Third HPO selection',
              value: 'DEFAULT',
            },
          ],
        },
        {
          title: 'Data Hub',
          formFields: [
            {
              type: 'select',
              label: 'Organisation type',
              value: 'LIMITED_COMPANY',
            },
            {
              type: 'select',
              label: 'Investment type',
              value: 'EXPANSION',
            },
            {
              type: 'text',
              label: 'Project name',
              value: 'ABC Hummingbird',
            },
            {
              type: 'textarea',
              label: 'Project description',
              value: 'Expansion of ABC Hummingbird factory sites',
            },
            {
              type: 'textarea',
              label: 'Anonymised project description',
              value: 'Expansion of factory sites',
            },
            {
              type: 'date',
              label: 'Estimated land date',
              value: '2021-02-03',
            },
            {
              type: 'select',
              label: 'New or existing investor',
              value: 'DEFAULT',
            },
            {
              type: 'select',
              label: 'Investor level of involvement',
              value: 'FDI_HUB_POST',
            },
            {
              type: 'select',
              label: 'Specific investment programme',
              value: 'IIGB',
            },
            {
              type: () =>
                cy.autocompleteFakeSelect(
                  'client_relationship_manager',
                  'Data Hub user 2',
                  'Data Hub user 2',
                  '/dh-adviser-search'
                ),
              label: 'Client Relationship Manager',
              value: 'Data Hub user 1',
            },
            {
              type: 'date',
              label: 'Date added to Data Hub',
              value: '2020-02-03',
            },
            {
              type: 'text',
              label: 'Project code',
              value: 'DHP-00000001',
            },
            {
              type: 'date',
              label: 'Project success date',
              value: '2022-02-03',
            },
            {
              type: 'textarea',
              label: 'Notes',
              value:
                'This is the notes section. The IST user can add any notes relating to the enquiry. This is a textarea and the user can input multiple lines of text.',
            },
          ],
        },
      ])
      cy.get('input[type=submit]').should('contain', 'Save and return')
      cy.get('form > a').eq(0).should('contain', 'Cancel')
      cy.get('form > a').eq(1).should('contain', 'Delete enquiry')
    })
  })

  context('when submitting new enquiry details', () => {
    it('should render the new details', () => {
      cy.populateForm([
        {
          type: 'text',
          name: 'company_name',
          value: '2Company',
        },
        {
          type: 'text',
          name: 'company_hq_address',
          value: 'DEF Electronics, USA',
        },
        {
          type: 'select',
          name: 'enquiry_stage',
          value: 'ENGAGED',
        },
        {
          type: 'select',
          name: 'owner',
          value: '2',
        },
        {
          type: 'select',
          name: 'investment_readiness',
          value: 'EXPLORING',
        },
        {
          type: 'select',
          name: 'quality',
          value: 'POTENTIALLY_NON_FDI',
        },
        {
          type: 'select',
          name: 'first_response_channel',
          value: 'EMAIL',
        },
        {
          type: 'text',
          name: 'website',
          value: 'https://www.caravans.com/',
        },
        {
          type: 'select',
          name: 'country',
          value: 'US',
        },
        {
          type: 'select',
          name: 'region',
          value: 'AMERICAS',
        },
        {
          type: 'select',
          name: 'primary_sector',
          value: 'AUTOMOTIVE',
        },
        {
          type: 'select',
          name: 'ist_sector',
          value: 'ENERGY',
        },
        {
          type: 'text',
          name: 'first_name',
          value: 'Johnny',
        },
        {
          type: 'text',
          name: 'last_name',
          value: 'Cakeman',
        },
        {
          type: 'text',
          name: 'email',
          value: 'johnny@cakeman.com',
        },
        {
          type: 'text',
          name: 'phone_country_code',
          value: '1234',
        },
        {
          type: 'text',
          name: 'phone',
          value: '+1 304 314 7000',
        },
        {
          type: 'select',
          name: 'request_for_call',
          value: 'YES_MORNING',
        },
        {
          type: 'text',
          name: 'google_campaign',
          value: '#r.4123426849_34553257',
        },
        {
          type: 'select',
          name: 'marketing_channel',
          value: 'LINKEDIN',
        },
        {
          type: 'select',
          name: 'how_they_heard_dit',
          value: 'SOCIAL_MEDIA',
        },
        {
          type: 'select',
          name: 'email_consent',
          value: 'False',
        },
        {
          type: 'select',
          name: 'phone_consent',
          value: 'True',
        },
        {
          type: 'select',
          name: 'first_hpo_selection',
          value: 'FOOD_PRODUCTION',
        },
        {
          type: 'select',
          name: 'second_hpo_selection',
          value: 'UK_RAIL',
        },
        {
          type: 'select',
          name: 'third_hpo_selection',
          value: 'LIGHTWEIGHT_STRUCTURES',
        },
        {
          type: 'select',
          name: 'organisation_type',
          value: 'LIMITED_COMPANY',
        },
        {
          type: 'select',
          name: 'investment_type',
          value: 'RETENTION',
        },
        {
          type: 'text',
          name: 'project_name',
          value: 'DEF Hummingbird',
        },
        {
          type: 'textarea',
          name: 'project_description',
          value: 'Expansion of DEF Hummingbird factory sites',
        },
        {
          type: 'textarea',
          name: 'anonymised_project_description',
          value: 'Expansion of more factory sites',
        },
        {
          type: 'date',
          name: 'estimated_land_date',
          value: '2020-01-02',
        },
        {
          type: 'select',
          name: 'new_existing_investor',
          value: 'EXISTING',
        },
        {
          type: 'select',
          name: 'investor_involvement_level',
          value: 'FDI_HUB_HQ_POST_LEP',
        },
        {
          type: 'select',
          name: 'specific_investment_programme',
          value: 'BUSINESS_PARTNER',
        },
        {
          type: () => {
            cy.autocompleteFakeSelect(
              'client_relationship_manager',
              'Data Hub user 2',
              'Data Hub user 2',
              '/dh-adviser-search'
            )
          },
          name: 'client_relationship_manager',
          value: 'Data Hub user 2',
        },
        {
          type: 'date',
          name: 'date_added_to_datahub',
          value: '2020-08-10',
        },
        {
          type: 'text',
          name: 'project_code',
          value: '67542',
        },
        {
          type: 'date',
          name: 'project_success_date',
          value: '2026-02-01',
        },
        {
          type: 'textarea',
          name: 'notes',
          value: 'This is the notes section thats all',
        },
      ])
      cy.get('input[type=submit]').eq(0).click()

      assertSummaryDetails([
        {
          title: '2Company',
          summaryList: [
            { dt: 'Date received', dd: '21 February 2020' },
            {
              dt: 'Date last updated',
              dd: format(new Date(), 'd MMMM yyyy'),
            },
            {
              dt: 'Enquiry stage',
              dd: 'Engaged in dialogue',
            },
            { dt: 'Owner', dd: 'Sam Koenen' },
            { dt: 'Company in Data Hub', dd: '----' },
          ],
        },
        {
          title: 'Enquiry details',
          summaryList: [
            { dt: 'Enquiry text' },
            {
              dt: 'Investment readiness',
              dd:
                'I’m still exploring where to expand my business and would like to know more about the UK’s offer',
            },
            { dt: 'Enquiry quality', dd: 'Potentially Non-FDI' },
            { dt: 'First response channel', dd: 'Email' },
          ],
        },
        {
          title: 'Company details',
          summaryList: [
            { dt: 'Website', dd: 'https://www.caravans.com/' },
            {
              dt: 'Country',
              dd: 'United States',
            },
            { dt: 'Region', dd: 'Americas' },
            {
              dt: 'Company HQ address',
              dd: 'DEF Electronics, USA',
            },
            { dt: 'Primary sector', dd: 'Automotive' },
            { dt: 'IST sector', dd: 'Energy and Environment' },
          ],
        },
        {
          title: 'Contact details',
          summaryList: [
            { dt: 'First name', dd: 'Johnny' },
            {
              dt: 'Last name',
              dd: 'Cakeman',
            },
            { dt: 'Job title', dd: 'Editor' },
            {
              dt: 'Email',
              dd: 'johnny@cakeman.com',
            },
            { dt: 'Phone', dd: '+1 304 314 7000' },
            { dt: 'Call requested', dd: 'Yes - morning' },
          ],
        },
        {
          title: 'Marketing information',
          summaryList: [
            { dt: 'Google campaign', dd: '#r.4123426849_34553257' },
            {
              dt: 'Marketing channel',
              dd: 'LinkedInLeadGen',
            },
            {
              dt: 'How did they hear about DIT?',
              dd: 'Other social media (e.g. Twitter/Facebook)',
            },
            {
              dt: 'Consent (email)',
              dd: 'Maybe',
            },
            { dt: 'Consent (telephone)', dd: 'Maybe' },
          ],
        },
        {
          title: 'HPO details',
          summaryList: [
            { dt: 'First HPO selection', dd: 'Food production' },
            {
              dt: 'Second HPO selection',
              dd: 'UK rail',
            },
            { dt: 'Third HPO selection', dd: 'Lightweight structures' },
          ],
        },
        {
          title: 'Data Hub details',
          summaryList: [
            { dt: 'Organisation type', dd: 'Limited company' },
            {
              dt: 'Investment type',
              dd: 'Retention',
            },
            { dt: 'Project name', dd: 'DEF Hummingbird' },
            {
              dt: 'Project description',
              dd: 'Expansion of DEF Hummingbird factory sites',
            },
            {
              dt: 'Anonymised project description',
              dd: 'Expansion of more factory sites',
            },
            { dt: 'Estimated land date', dd: '02 January 2020' },
            { dt: 'New or existing investor', dd: 'Existing Investor' },
            {
              dt: 'Investor level of involvement',
              dd: 'FDI Hub + HQ + Post + LEP',
            },
            {
              dt: 'Specific investment programme',
              dd: 'Business Partnership (Non-FDI)',
            },
            { dt: 'Client Relationship Manager', dd: 'Data Hub user 2' },
            { dt: 'Date added to Data Hub', dd: '10 August 2020' },
            { dt: 'Project code', dd: '67542' },
            { dt: 'Project success date', dd: '01 February 2026' },
          ],
        },
        {
          title: 'Notes',
          summaryList: [
            {
              dt: 'Notes',
              dd: 'This is the notes section thats all',
            },
          ],
        },
      ])
    })
  })
})
