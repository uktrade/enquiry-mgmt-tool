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
      cy.wrap($el)
        .find('dt')
        .should('contain', specs[i].dt)
        .next()
        .should('contain', specs[i].dd)
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
        sectionFields.type === 'address'
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

module.exports = {
  assertSummaryList,
  assertEnquiryForm,
  assertSummaryDetails,
}
