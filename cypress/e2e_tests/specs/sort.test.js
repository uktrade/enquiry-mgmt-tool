require('../support/commands')
const { assertSortedByDate } = require('../support/assertions')
const { sort } = require('../selectors')

const FIELDINDEXES = {
  'date_received': 1,
  'date_updated': 3,
}

const testDateSort = (searchString, fieldIndex, ascending) => {
  context(`Sorting by ${searchString}`, () => {
    it(`Should sort enquiries in ${ascending ? 'ascending': 'descending'} order`, () => {
      cy.get(sort.selector).select(searchString)
      assertSortedByDate(fieldIndex, ascending);
    })
  })
}

describe('Sorting enquiries list view', () => {
  before(() => {
    cy.reseed('/')
  })
  beforeEach(() => Cypress.Cookies.preserveOnce('sessionid'))

  context('Viewing without explicit sorting', () => {
    it('Should sort enquiries by newest date received', () => {
      assertSortedByDate(FIELDINDEXES.date_received, false);
    })
  })

  testDateSort('Most recently updated', FIELDINDEXES.date_updated, false)

  testDateSort('Least recently received', FIELDINDEXES.date_received, true)

  testDateSort('Most recently received', FIELDINDEXES.date_received, false)


  context('Sorting by Company name: A-Z', () => {
    it('Should sort enquiries in ascending order', () => {
      cy.get(sort.selector).select('Company name: A-Z')

      cy.get(sort.companyName)
        .then(($els) => {
          const names = $els.map($el => $el.text)
          expect(names).to.eq(names.sort((a, b) => {a.localeCompare(b)}))
        })
    })
  })
})
