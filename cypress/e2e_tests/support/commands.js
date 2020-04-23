Cypress.Commands.add('findDetailsSection', number => cy.get('main').find('div > div').eq(number).find('h3'))
