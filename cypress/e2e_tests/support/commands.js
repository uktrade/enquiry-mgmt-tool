Cypress.Commands.add('findDetailsSection', number =>
  cy
    .get('main')
    .find('div > div')
    .eq(number)
    .find(number === 0 ? 'h2' : 'h3')
)

const populateField = (type, name, value) => {
  if (typeof type === 'function') {
    return type()
  }
  switch (type) {
    case 'select':
      return cy.get(`select[name=${name}]`).select(value)
    case 'textarea':
      return cy.get(`textarea[name=${name}]`).clear().type(value)
    default:
      return cy.get(`input[name=${name}]`).clear().type(value)
  }
}

Cypress.Commands.add('populateForm', formFieldsData => {
  formFieldsData.forEach(({ type, name, value }) => {
    populateField(type, name, value)
  })
})

Cypress.Commands.add('reseed', path => {
  cy.request('POST', '/testfixtureapi/reset-fixtures/', {
    username: 'testuser',
    first_name: 'testuserfirstname',
    last_name: 'testuserlastname',
    email: 'test@test.com',
  })
  cy.visit(path)
})

Cypress.Commands.add('autocompleteFakeSelect', (name, label, value, path) => {
    cy.server()
    cy.route({
      method: 'GET',
      url: path,
      response: {
        results: [
          {text: label, id: value},
        ],
      }
    })

    cy.get(`#select2-id_${name}-container`)
      .click()

    cy.get(`#select2-id_${name}-results`)
      .within(() => {
        cy.contains(label).click()
      })
})
