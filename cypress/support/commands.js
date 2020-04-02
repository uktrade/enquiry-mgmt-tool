Cypress.Commands.add('login', (next = '/', username='testuser', password='testpass') => {
    cy.visit(`/admin/login/?next=${next}`)
    cy.get('input[name=username]').type(username)
    cy.get('input[name=password]').type(password)
    cy.contains('Log in').click()
})
