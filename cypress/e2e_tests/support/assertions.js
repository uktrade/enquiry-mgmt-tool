const NOT_EDITABLE = 'NOT_EDITABLE'

const assertSummaryDetails = specs => {
  cy.get('main div > div').each(($div, i) => {
    const header = i === 0 ? 'h2' : 'h3'
    cy.wrap($div)
      .find(header)
      .contains(specs[i].title)
      .next()
      .then($dl => assertSummaryList($dl, specs[i].summaryList))
  })
}

const assertSummaryList = ($element, specs) => {
  cy.wrap($element)
    .find('div')
    .each(($el, i) => {
      const spec = specs[i]

      if (!spec.dd) {
          return
      }

      cy.wrap($el)
        .find('dt')
        .should('contain', spec.dt)
        .next()
        .should('contain', spec.dd)
    })
}

const assertEnquiryForm = specs => {
  const inputType = type =>
    type === 'text' ? ['have.attr', 'value'] : ['have.value']

  cy.get('main form > div').each(($element, sectionIndex) => {
    const section = specs[sectionIndex]
    cy.wrap($element)
      .find('h3')
      .should('have.text', section.title)
      .parent()
      .find('> div')
      .each(($div, index) => {
        const sectionFields = section.formFields[index]
        sectionFields.type === NOT_EDITABLE
          ? cy
              .wrap($div)
              .contains('div', sectionFields.label)
              .parent()
              .contains('p', sectionFields.value)

          : sectionFields.type === 'address'
            ? cy
                .wrap($div)
                .contains('label', sectionFields.label)
                .parent()
                .find('div')
                .eq(2)
                .should('contain', sectionFields.address)
            : cy
                .wrap($div)
                .contains('label', sectionFields.label)
                .next()
                .should(...inputType(sectionFields.type), sectionFields.value)
      })
  })
}

const assertSortedByDate = (fieldIndex, ascending) => {
  cy.get(`.entity__content-item:nth-child(${fieldIndex}) .list-item-value`)
    .then(($els) => {
      const dates = $els.map($el => Date.parse($el.text))
      expect(dates).to.eq(dates.sort((a, b) => { ascending ? a < b : a > b }))
    })
}

module.exports = {
  assertSummaryList,
  assertEnquiryForm,
  assertSummaryDetails,
  assertSortedByDate,
  NOT_EDITABLE,
}
