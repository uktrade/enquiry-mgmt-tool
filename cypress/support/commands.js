Cypress.Commands.add('login', (next = '?', username='trusted_user', password='testpass') => {
    cy.visit(`/admin/login/?next=${next}`)
    cy.get('input[name=username]').type(username)
    cy.get('input[name=password]').type(password)
    cy.contains('Log in').click()
})

Cypress.Commands.add('viewEnquiry', (id) => {
    cy.visit(`/enquiries/${id}/`)
})

Cypress.Commands.add('editEnquiry', (id) => {
    cy.visit(`/enquiries/${id}/edit`)
})
