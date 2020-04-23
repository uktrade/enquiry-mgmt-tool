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

module.exports = {
  assertSummaryList,
}
