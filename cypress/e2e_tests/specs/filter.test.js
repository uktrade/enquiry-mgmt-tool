require('../support/commands')
const usersFixture = require('../../../app/enquiries/fixtures/test_users.json')
const enquiriesFixture = require('../../../app/enquiries/fixtures/test_enquiries.json')

const USERS = usersFixture.reduce(
  (a, {pk, fields: {first_name, last_name}}) => ({
    ...a,
    [pk]: `${first_name} ${last_name}`,
  }),
  {},
)

// The result list items only show a subset of the enquiry data and we need
// to make assertions about the information not shown. The constants
// ENQUIRIES and ENQUIRERS constants are maps of primary keys to enquiries and
// enquirers fixtures respectively, which we are using to make assertions.
const fixtureReducer = (a, {pk, fields}) => ({ ...a, [pk]: fields })
const ENQUIRIES = enquiriesFixture
  .filter(({model}) => model === 'enquiries.enquiry')
  .reduce(fixtureReducer, {})
const ENQUIRERS = enquiriesFixture
  .filter(({model}) => model === 'enquiries.enquirer')
  .reduce(fixtureReducer, {})

const FILTERS = {
  new: 'New',
  added: 'Added to Data Hub',
  nonFdi: 'Non-FDI',
  nonResponsive: 'Non-responsive',
  awaiting: 'Awaiting response from Investor',
  postProgressing: 'Post progressing',
  sent: 'Sent to Post',
  engaged: 'Engaged in dialogue',
}

const filterLabels = filters =>
  Object.entries(filters)
    .map(([k, v]) =>
      typeof v === 'string'
        ? `${k}: ${v}`
        : k
     )
    .join(', ')

const getInputByLabel = (label) =>
  cy.contains('label', label)
    .parent()
    .find('input')

const clearFilters = () =>
  cy.contains('Clear filters')
    .click()

const setFilters = filters => {
  clearFilters()
  Object.entries(filters).forEach(([label, val]) => {
    const input = getInputByLabel(label)
    typeof val === 'string'
      ? val === ''
        // Date input doesn't allow empty string to be typed in
        ? input.clear()
        : input.type(val)
      : val
        ? input.check()
        : input.uncheck()
  })
}

const assertFiltersSet = filters =>
  Object.entries(filters).forEach(([label, val]) =>
    typeof val === 'string'
      ? getInputByLabel(label).should('have.value', val)
      : getInputByLabel(label).should('have.prop', 'checked', val)
  )

const submitFilters = () =>
  cy.contains('Apply filters')
    .as('submit')
    .click()

const assertPage = (itemsPerPage, assert = () => {}) =>
  cy.get('article')
    .find('ol li')
    .as('items')
    .should('have.length', itemsPerPage)
    .each(assert)

const testResults = (assert, expectedTotal, testPages) => {
  context('Results', () => {
    it(`Should show ${expectedTotal} total results`, () =>
      cy.get('header')
        .contains(`${expectedTotal} enquiries`)
    )

    if (!testPages) {
      return
    }

    const r = expectedTotal % 10
    const pages = [...Array((expectedTotal - r) / 10).fill(10), r]

    pages.forEach((itemsPerPage, i) => {
      const currentPage = i + 1
      const nextPage = i + 2

      it(`Page ${currentPage}`, () => {
        assertPage(itemsPerPage, assert)
        currentPage < pages.length && cy.get('.pagination')
          .contains('a', `${nextPage}`)
          .click()
      })
    })

    pages.slice(0, -1).reverse().forEach(itemsPerPage =>
      it(`Should show ${itemsPerPage} when clicking Previous`, () => {
        cy.get('.pagination')
          .contains('Previous')
          .click()

        assertPage(itemsPerPage, assert)
      })
    )

    pages.slice(1).forEach(itemsPerPage =>
      it(`Should show ${itemsPerPage} when clicking Next`, () => {
        cy.get('.pagination')
          .contains('Next')
          .click()

        assertPage(itemsPerPage, assert)
      })
    )
  })
}

const testFilters = ({
  filters,
  assertItem,
  expectedTotal,
  testFilteredPages,
  testUnfilteredPages,
  testUnfiltered,
}) => {
  describe(`Filter by: ${filterLabels(filters)}`, () => {
    context('With filters applied', () => {
      it('Set filters', () => {
        setFilters(filters)
        submitFilters()
      })

      testResults(assertItem, expectedTotal, testFilteredPages)
    })

    testUnfiltered && context(
      'Removing filters should bring back unfiltered results',
      () => {
        it('Reset filters', () => {
          clearFilters()
          submitFilters()
        })

        testResults(() => {}, Object.keys(ENQUIRIES).length, testUnfilteredPages)
      })
    })
}

const testPagination = ({ filters, totalPages, pages }) =>
  it('Should preserve filter when paginating', () => {
    setFilters(filters)
    submitFilters()
    pages.forEach(({ linkLabel, pageNo }) => {
      cy.get('.pagination').contains(linkLabel).click()
      cy.get('header').contains(`Page ${pageNo} of ${totalPages}`)
      assertFiltersSet(filters)
    })
  })

describe('Filters', () => {
  before(() => {
    cy.reseed('/enquiries/')
  })
  beforeEach(() => Cypress.Cookies.preserveOnce('sessionid'))

  testPagination({
    filters: {
      'Received before': '2020-01-01',
      'New': true,
      'Awaiting response from Investor': true,
      'Engaged in dialogue': true,
      'Non-responsive': true,
      'Added to Data Hub': true,
      'Post progressing': true,
    },
    totalPages: 3,
    pages: [
      {linkLabel: 'Next', pageNo: 2},
      {linkLabel: 'Previous', pageNo: 1},
      {linkLabel: 3, pageNo: 3},
      {linkLabel: 2, pageNo: 2},
      {linkLabel: 1, pageNo: 1},
    ],
  })

  testPagination({
    filters: {
      'Received after': '2000-01-01',
      'Company added to Data Hub before': '2020-05-31',
      'Company added to Data Hub after': '1970-01-01',
      'Unassigned': true,
      [USERS[1]]: true,
      [USERS[3]]: true,
      [USERS[5]]: true,
    },
    totalPages: 3,
    pages: [
      {linkLabel: 'Next', pageNo: 2},
      {linkLabel: 'Previous', pageNo: 1},
      {linkLabel: 3, pageNo: 3},
      {linkLabel: 2, pageNo: 2},
      {linkLabel: 1, pageNo: 1},
    ],
  })

  testFilters({
    filters: {
      New: true,
    },
    expectedTotal: 11,
    testFilteredPages: true,
    testUnfiltered: true,
    testUnfilteredPages: true,
    assertItem: ($li) => cy.wrap($li).contains(/^New$/),
  })
  testFilters({
    filters: {
      New: true,
      [USERS[1]]: true,
      [USERS[2]]: true,
    },
    expectedTotal: 2,
    assertItem: ($li) => {
      cy.wrap($li).contains(/^New$/)
      cy.wrap($li).contains(/(^\s*IST User (1|2)\s*$)/)
    },
  })

  testFilters({
    filters: {
      [FILTERS.awaiting]: true,
    },
    expectedTotal: 8,
    assertItem: ($li) =>
      cy.wrap($li).contains(/^Awaiting response from Investor$/),
  })
  testFilters({
    filters: {
      [FILTERS.awaiting]: true,
      [USERS[5]]: true,
    },
    expectedTotal: 6,
    assertItem: ($li) => {
      cy.wrap($li).contains(/^Awaiting response from Investor$/)
      cy.wrap($li).contains(/(^\s*IST User 5\s*$)/)
    },
  })

  testFilters({
    filters: {
      [FILTERS.engaged]: true,
    },
    expectedTotal: 0,
    assertItem: () => {},
  })
  testFilters({
    filters: {
      [FILTERS.engaged]: true,
      [USERS[5]]: true,
    },
    expectedTotal: 0,
    assertItem: () => {},
  })
  
  testFilters({
    filters: {
      [FILTERS.nonResponsive]: true,
    },
    expectedTotal: 5,
    assertItem: ($li) => cy.wrap($li).contains(/^Non-responsive$/),
  })
  testFilters({
    filters: {
      [FILTERS.nonResponsive]: true,
      [USERS[4]]: true,
    },
    expectedTotal: 5,
    assertItem: ($li) => {
      cy.wrap($li).contains(/^Non-responsive$/)
      cy.wrap($li).contains(/(^\s*IST User 4\s*$)/)
    },
  })
  
  testFilters({
    filters: {
      [FILTERS.nonFdi]: true,
    },
    expectedTotal: 5,
    assertItem: ($li) => cy.wrap($li).contains(/^Non-FDI$/),
  })
  testFilters({
    filters: {
      [FILTERS.nonFdi]: true,
      Unassigned: true,
    },
    expectedTotal: 1,
    assertItem: ($li) => {
      cy.wrap($li).contains(/^Non-FDI$/)
      cy.wrap($li).contains(/(^\s*Unassigned\s*$)/)
    },
  })
  
  testFilters({
    filters: {
      [FILTERS.added]: true,
    },
    expectedTotal: 3,
    assertItem: ($li) => cy.wrap($li).contains(/^Added to Data Hub$/),
  })
  testFilters({
    filters: {
      [FILTERS.added]: true,
      [USERS[2]]: true,
    },
    expectedTotal: 3,
    assertItem: ($li) => {
      cy.wrap($li).contains(/^Added to Data Hub$/)
      cy.wrap($li).contains(/(^\s*IST User 2\s*$)/)
    },
  })
  testFilters({
    filters: {
      [FILTERS.added]: true,
      Unassigned: true,
      [USERS[1]]: true,
      [USERS[3]]: true,
      [USERS[4]]: true,
      [USERS[5]]: true,
    },
    expectedTotal: 0,
    assertItem: () => {},
  })
  
  testFilters({
    filters: {
      [FILTERS.sent]: true,
    },
    expectedTotal: 2,
    assertItem: ($li) => cy.wrap($li).contains(/^Sent to Post$/),
  })
  testFilters({
    filters: {
      [FILTERS.sent]: true,
      [USERS[5]]: true,
    },
    expectedTotal: 1,
    assertItem: ($li) => {
      cy.wrap($li).contains(/^Sent to Post$/)
      cy.wrap($li).contains(/(^\s*IST User 5\s*$)/)
    },
  })
  testFilters({
    filters: {
      [FILTERS.sent]: true,
      Unassigned: true,
    },
    expectedTotal: 1,
    assertItem: ($li) => {
      cy.wrap($li).contains(/^Sent to Post$/)
      cy.wrap($li).contains(/(^\s*Unassigned\s*$)/)
    },
  })
  
  testFilters({
    filters: {
      [FILTERS.postProgressing]: true,
    },
    expectedTotal: 3,
    assertItem: ($li) => cy.wrap($li).contains(/^Post progressing$/),
  })
  testFilters({
    filters: {
      [FILTERS.postProgressing]: true,
      [USERS[1]]: true,
    },
    expectedTotal: 1,
    assertItem: ($li) => {
      cy.wrap($li).contains(/^Post progressing$/)
      cy.wrap($li).contains(/(^\s*IST User 1\s*$)/)
    },
  })
  testFilters({
    filters: {
      [FILTERS.postProgressing]: true,
      Unassigned: true,
    },
    expectedTotal: 2,
    assertItem: ($li) => {
      cy.wrap($li).contains(/^Post progressing$/)
      cy.wrap($li).contains(/(^\s*Unassigned\s*$)/)
    },
  })
  
  testFilters({
    filters: {
      Unassigned: true,
    },
    expectedTotal: 14,
    assertItem: ($li) => cy.wrap($li).contains(/(^\s*Unassigned\s*$)/),
  })
  testFilters({
    filters: {
      Unassigned: true,
      [FILTERS.new]: true,
    },
    expectedTotal: 8,
    assertItem: ($li) => {
      cy.wrap($li).contains(/^New$/)
      cy.wrap($li).contains(/(^\s*Unassigned\s*$)/)
    },
  })
  
  testFilters({
    filters: {
      [USERS[1]]: true,
    },
    expectedTotal: 2,
    assertItem: ($li) => cy.wrap($li).contains(/(^\s*IST User 1\s*$)/),
  })
  testFilters({
    filters: {
      [USERS[1]]: true,
      [FILTERS.new]: true,
    },
    expectedTotal: 1,
    assertItem: ($li) => {
      cy.wrap($li).contains(/^New$/)
      cy.wrap($li).contains(/(^\s*IST User 1\s*$)/)
    },
  })
  
  testFilters({
    filters: {
      [USERS[2]]: true,
    },
    expectedTotal: 4,
    assertItem: ($li) => cy.wrap($li).contains(/(^\s*IST User 2\s*$)/),
  })
  testFilters({
    filters: {
      [USERS[2]]: true,
      [FILTERS.added]: true,
    },
    expectedTotal: 3,
    assertItem: ($li) => {
      cy.wrap($li).contains(/^Added to Data Hub$/)
      cy.wrap($li).contains(/(^\s*IST User 2\s*$)/)
    },
  })
  
  testFilters({
    filters: {
      [USERS[3]]: true,
    },
    expectedTotal: 5,
    assertItem: ($li) => cy.wrap($li).contains(/(^\s*IST User 3\s*$)/),
  })
  testFilters({
    filters: {
      [USERS[3]]: true,
      [FILTERS.nonFdi]: true,
    },
    expectedTotal: 4,
    assertItem: ($li) => {
      cy.wrap($li).contains(/^Non-FDI$/)
      cy.wrap($li).contains(/(^\s*IST User 3\s*$)/)
    },
  })
  
  testFilters({
    filters: {
      [USERS[4]]: true,
    },
    expectedTotal: 5,
    assertItem: ($li) => cy.wrap($li).contains(/(^\s*IST User 4\s*$)/),
  })
  testFilters({
    filters: {
      [USERS[4]]: true,
      [FILTERS.nonResponsive]: true,
    },
    expectedTotal: 5,
    assertItem: ($li) => {
      cy.wrap($li).contains(/^Non-responsive$/)
      cy.wrap($li).contains(/(^\s*IST User 4\s*$)/)
    },
  })
  testFilters({
    filters: {
      [USERS[4]]: true,
      [FILTERS.new]: true,
      [FILTERS.awaiting]: true,
      [FILTERS.engaged]: true,
      [FILTERS.nonFdi]: true,
      [FILTERS.added]: true,
      [FILTERS.sent]: true,
      [FILTERS.postProgressing]: true,
    },
    expectedTotal: 0,
  })
  
  testFilters({
    filters: {
      [USERS[5]]: true,
    },
    expectedTotal: 7,
    assertItem: ($li) => cy.wrap($li).contains(/(^\s*IST User 5\s*$)/),
  })
  testFilters({
    filters: {
      [USERS[5]]: true,
      [FILTERS.awaiting]: true,
    },
    expectedTotal: 6,
    assertItem: ($li) => {
      cy.wrap($li).contains(/^Awaiting response from Investor$/)
      cy.wrap($li).contains(/(^\s*IST User 5\s*$)/)
    },
  })
  
  testFilters({
    filters: {
      'Received before': '2018-01-01',
    },
    expectedTotal: 11,
    testFilteredPages: true,
    assertItem: ($li) =>
      cy.wrap($li)
        .contains('Date received')
        .next()
        .then($el =>
          expect(new Date($el.text())).to.be.below(new Date('2018-01-01'))
        ),
  })
  
  testFilters({
    filters: {
      'Received after': '2019-01-01',
    },
    expectedTotal: 13,
    testFilteredPages: true,
    assertItem: ($li) =>
      cy.wrap($li)
        .contains('Date received')
        .next()
        .then($el =>
          expect(new Date($el.text())).to.be.above(new Date('2001-01-01'))
        ),
  })
  
  testFilters({
    filters: {
      'Received before': '2018-01-01',
      'Received after': '2017-07-01',
    },
    expectedTotal: 5,
    assertItem: ($li) =>
      cy.wrap($li)
        .contains('Date received')
        .next()
        .then($el =>
          expect(new Date($el.text())).to.be.within(
            new Date('2017-07-01'),
            new Date('2018-01-01'),
          )
        ),
  })
  
  Object.entries({
    matchbox: [6, 3],
    company: [10, 2],
    ltd: [16, 6],
    mars: [5, 1],
    a: [32, 9],
    foo: [0, 0],
  }).forEach(([term, [total, totalNew]]) => {
    testFilters({
      filters: {
        'Company name': term,
      },
      expectedTotal: total,
      assertItem: ($li) => cy.wrap($li).contains(term, {matchCase: false}),
    })
    testFilters({
      filters: {
        'Company name': term,
        [FILTERS.new]: true,
      },
      expectedTotal: totalNew,
      assertItem: ($li) => {
        cy.wrap($li).contains(term, {matchCase: false})
        cy.wrap($li).contains(/^New$/)
      },
    })
  })
  
  Object.entries({
    'evelyn.wang@example.com': 13,
    'jeff.bezos@washingtonpost.com': 12,
    'nanny.maroon@bluemountain.jm': 12,
  }).forEach(([email, total]) =>
    testFilters({
      filters: {
        'Enquirer email address': email,
      },
      expectedTotal: total,
      assertItem: ($li) => {
        cy.wrap($li).find('a').then($el => {
          // The enquirer information is not available on the result item,
          // so we will read it directly from the fixture by primary key.
          const pk = $el.attr('href').match(/\d+/)[0]
          const enquiry = ENQUIRIES[pk]
          const enquirer = ENQUIRERS[enquiry.enquirer]
          expect(enquirer.email).to.eq(email)
        })
      },
    })
  )
  
  testFilters({
    filters: {
      'Company added to Data Hub before': '2020-02-04',
    },
    expectedTotal: 37,
    assertItem: ($li) => {
      cy.wrap($li).find('a').then($el => {
        // The added to Data Hub date is not available on the result item,
        // so we will read it directly from the fixture by primary key.
        const pk = $el.attr('href').match(/\d+/)[0]
        const enquiry = ENQUIRIES[pk]
        expect(new Date(enquiry.date_added_to_datahub))
          .to.be.below(new Date('2020-02-04'))
      })
    },
  })
  
  testFilters({
    filters: {
      'Company added to Data Hub before': '2020-02-03',
    },
    expectedTotal: 0,
  })
  
  testFilters({
    filters: {
      'Company added to Data Hub after': '2020-02-02',
    },
    expectedTotal: 37,
    testFilteredPages: true,
    assertItem: ($li) => {
      cy.wrap($li).find('a').then($el => {
        const pk = $el.attr('href').match(/\d+/)[0]
        const enquiry = ENQUIRIES[pk]
        expect(new Date(enquiry.date_added_to_datahub))
          .to.be.above(new Date('2020-02-02'))
      })
    },
  })
  
  testFilters({
    filters: {
      'Company added to Data Hub after': '2020-02-03',
    },
    expectedTotal: 0,
  })
})
