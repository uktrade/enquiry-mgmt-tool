Cypress.Commands.add('findDetailsSection', number => {
  return number === 0
    ? cy.get('main').find('div > div').eq(number).find('h2')
    : cy.get('main').find('div > div').eq(number).find('h3')
})

const populateField = (type, name, value) => {
  const fieldTypes = {
    select: () => cy.get(`select[name=${name}]`).select(value),
    textarea: () => cy.get(`textarea[name=${name}]`).clear().type(value),
    default: () => cy.get(`input[name=${name}]`).clear().type(value),
  }
  return typeof fieldTypes[type] !== 'function'
    ? fieldTypes['default']()
    : fieldTypes[type]()
}

Cypress.Commands.add('populateForm', formFieldsData => {
  formFieldsData.forEach(({ type, name, value }) => {
    populateField(type, name, value)
  })
})
