const { format } = require("date-fns");
require("../support/commands");
const {
  assertSummaryDetails,
  assertEnquiryForm,
  NOT_EDITABLE,
} = require("../support/assertions");
const { results, details } = require("../selectors");

describe("Edit", () => {
  before(() => {
    cy.visit("/");
  });

  beforeEach(() => {
    Cypress.Cookies.preserveOnce("sessionid");
    Cypress.Cookies.preserveOnce("csrftoken");
    Cypress.Cookies.debug(true);
  });

  context("when viewing the enquiry details", () => {
    it("should render the details", () => {
      cy.get(results.number(1)).find("h3 a").click();
      cy.get(details.topControls)
        .find("a")
        .eq(0)
        .should("have.text", "Back")
        .and("have.attr", "href", "/")
        .parents()
        .find("a")
        .should("contain", "Edit details");

      assertSummaryDetails([
        {
          title: "ABC Electronics Co. (long text)",
          summaryList: [
            { dt: "Date received", dd: "05 May 2024" },
            {
              dt: "Date last updated",
              dd: "15 May 2024",
            },
            {
              dt: "Enquiry stage",
              dd: "Engaged in dialogue",
            },
            { dt: "Owner", dd: "James Curran" },
            { dt: "Company in Data Hub", dd: "----" },
          ],
        },
        {
          title: "Enquiry details",
          summaryList: [
            {
              dt: "Enquiry text",
              dd: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure...",
            },
            {
              dt: "Investment readiness",
              dd: "I’m still exploring where to expand my business and would like to know more about the UK’s offer",
            },
            { dt: "Enquiry quality", dd: "Potentially Non-FDI" },
            { dt: "First response channel", dd: "Email" },
          ],
        },
        {
          title: "Company details",
          summaryList: [
            { dt: "Website", dd: "https://www.caravans.com/" },
            {
              dt: "Country",
              dd: "United States",
            },
            { dt: "Region", dd: "Americas" },
            {
              dt: "Company HQ address",
              dd: "ABC Electronics Co. (UK), Far Far Away, United Kingdom",
            },
            { dt: "Primary sector", dd: "Automotive" },
            { dt: "IST sector", dd: "Energy and Environment" },
          ],
        },
        {
          title: "Contact details",
          summaryList: [
            { dt: "First name", dd: "Neo" },
            {
              dt: "Last name",
              dd: "Pug",
            },
            { dt: "Job title", dd: "Director" },
            {
              dt: "Email",
              dd: "neopug@example.com",
            },
            { dt: "Phone", dd: "+1 304 314 7000" },
            { dt: "Call requested", dd: "Yes - morning" },
          ],
        },
        {
          title: "Marketing information",
          summaryList: [
            { dt: "Google campaign", dd: "#r.4123426849_34553257" },
            {
              dt: "Marketing channel",
              dd: "LinkedInLeadGen",
            },
            {
              dt: "How did they hear about DBT?",
              dd: "Other social media (e.g. Twitter/Facebook)",
            },
            {
              dt: "Consent (email)",
              dd: "No",
            },
            { dt: "Consent (telephone)", dd: "No" },
          ],
        },
        {
          title: "HPO details",
          summaryList: [
            { dt: "First HPO selection", dd: "Food production" },
            {
              dt: "Second HPO selection",
              dd: "UK rail",
            },
            { dt: "Third HPO selection", dd: "Lightweight structures" },
          ],
        },
        {
          title: "Data Hub details",
          summaryList: [
            { dt: "Organisation type", dd: "Limited company" },
            {
              dt: "Investment type",
              dd: "Retention",
            },
            { dt: "Project name", dd: "DEF Hummingbird" },
            {
              dt: "Project description",
              dd: "Expansion of DEF Hummingbird factory sites",
            },
            {
              dt: "Anonymised project description",
              dd: "Expansion of more factory sites",
            },
            { dt: "Estimated land date", dd: "02 January 2020" },
            { dt: "New or existing investor", dd: "Existing Investor" },
            {
              dt: "Investor level of involvement",
              dd: "FDI Hub + HQ + Post + LEP",
            },
            {
              dt: "Specific investment programme",
              dd: "Business Partnership (Non-FDI)",
            },
            { dt: "Client Relationship Manager", dd: "Aaron Norris" },
            { dt: "Date added to Data Hub", dd: "10 August 2020" },
            { dt: "Project code", dd: "67542" },
            { dt: "Project success date", dd: "01 February 2026" },
          ],
        },
        {
          title: "Notes",
          summaryList: [
            {
              dt: "Notes",
              dd: "This is the notes section. The IST user can add any notes relating to the enquiry. This is a textarea and the user can input multiple lines of text.",
            },
          ],
        },
      ]);
    });
  });

  context("when editing the enquiry", () => {
    it("should render the form", () => {
      cy.get(details.editDetailsButton).click();
      assertEnquiryForm([
        {
          title: "Enquiry overview",
          formFields: [
            {
              type: "text",
              label: "Company name",
              value: "ABC Electronics Co. (long text)",
            },
            {
              type: "text",
              label: "Company HQ address",
              value: "ABC Electronics Co. (UK), Far Far Away, United Kingdom",
            },
            {
              type: "select",
              label: "Enquiry stage",
              value: "ENGAGED",
            },
            {
              type: "select",
              label: "Owner",
              value: "2",
            },
            {
              type: "address",
              label: "Company in Data Hub",
              address: "",
            },
          ],
        },
        {
          title: "Enquiry details",
          formFields: [
            {
              type: NOT_EDITABLE,
              label: "Enquiry text",
              value:
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure...",
            },
            {
              type: "select",
              label: "Investment readiness",
              value: "EXPLORING",
            },
            {
              type: "select",
              label: "Enquiry quality",
              value: "POTENTIALLY_NON_FDI",
            },
            {
              type: "select",
              label: "First response channel",
              value: "EMAIL",
            },
          ],
        },
        {
          title: "Company details",
          formFields: [
            {
              type: "text",
              label: "Website",
              value: "https://www.caravans.com/",
            },
            {
              type: "select",
              label: "Country",
              value: "US",
            },
            {
              type: "select",
              label: "Region",
              value: "AMERICAS",
            },
            {
              type: "select",
              label: "Primary sector",
              value: "AUTOMOTIVE",
            },
            {
              type: "select",
              label: "IST sector",
              value: "ENERGY",
            },
          ],
        },
        {
          title: "Contact",
          formFields: [
            {
              type: "text",
              label: "First name",
              value: "Neo",
            },
            {
              type: "text",
              label: "Last name",
              value: "Pug",
            },
            {
              type: "text",
              label: "Job title",
              value: "Director",
            },
            {
              type: "text",
              label: "Email",
              value: "neopug@example.com",
            },
            {
              type: "text",
              label: "Telephone country code",
              value: "1234",
            },
            {
              type: "text",
              label: "Phone",
              value: "+1 304 314 7000",
            },
            {
              type: "select",
              label: "Call requested",
              value: "YES_MORNING",
            },
          ],
        },
        {
          title: "Marketing",
          formFields: [
            {
              type: "text",
              label: "Google campaign",
              value: "#r.4123426849_34553257",
            },
            {
              type: "select",
              label: "Marketing channel",
              value: "LINKEDIN",
            },
            {
              type: "select",
              label: "How did they hear about DBT?",
              value: "SOCIAL_MEDIA",
            },
            {
              type: "select",
              label: "Consent (email)",
              value: "False",
            },
            {
              type: "select",
              label: "Consent (telephone)",
              value: "False",
            },
          ],
        },
        {
          title: "HPO details",
          formFields: [
            {
              type: "select",
              label: "First HPO selection",
              value: "FOOD_PRODUCTION",
            },
            {
              type: "select",
              label: "Second HPO selection",
              value: "UK_RAIL",
            },
            {
              type: "select",
              label: "Third HPO selection",
              value: "LIGHTWEIGHT_STRUCTURES",
            },
          ],
        },
        {
          title: "Data Hub",
          formFields: [
            {
              type: "select",
              label: "Organisation type",
              value: "LIMITED_COMPANY",
            },
            {
              type: "select",
              label: "Investment type",
              value: "RETENTION",
            },
            {
              type: "text",
              label: "Project name",
              value: "DEF Hummingbird",
            },
            {
              type: "textarea",
              label: "Project description",
              value: "Expansion of DEF Hummingbird factory sites",
            },
            {
              type: "textarea",
              label: "Anonymised project description",
              value: "Expansion of more factory sites",
            },
            {
              type: "date",
              label: "Estimated land date",
              value: "2020-01-02",
            },
            {
              type: "select",
              label: "New or existing investor",
              value: "EXISTING",
            },
            {
              type: "select",
              label: "Investor level of involvement",
              value: "FDI_HUB_HQ_POST_LEP",
            },
            {
              type: "select",
              label: "Specific investment programme",
              value: "BUSINESS_PARTNER",
            },
            {
              type: () => {
                cy.autocompleteFakeSelect(
                  "client_relationship_manager",
                  "Aaron Norris",
                  "Aaron Norris",
                  "/dh-adviser-search"
                );
              },
              label: "Client Relationship Manager",
              value: "Aaron Norris",
            },
            {
              type: "date",
              label: "Date added to Data Hub",
              value: "2020-08-10",
            },
            {
              type: "text",
              label: "Project code",
              value: "67542",
            },
            {
              type: "date",
              label: "Project success date",
              value: "2026-02-01",
            },
            {
              type: "textarea",
              label: "Notes",
              value:
                "This is the notes section. The IST user can add any notes relating to the enquiry. This is a textarea and the user can input multiple lines of text.",
            },
          ],
        },
      ]);
      cy.get("input[type=submit]").should("contain", "Save and return");
      cy.get("form > a").eq(0).should("contain", "Cancel");
      cy.get("form > a").eq(1).should("contain", "Delete enquiry");
    });
  });

  context("when submitting new enquiry details", () => {
    it("should render the new details", () => {
      cy.populateForm([
        {
          type: "text",
          name: "company_name",
          value: "ABC Electronics Co. (long text)",
        },
        {
          type: "text",
          name: "company_hq_address",
          value: "ABC Electronics Co. (UK), Far Far Away, United Kingdom",
        },
        {
          type: "select",
          name: "enquiry_stage",
          value: "ENGAGED",
        },
        {
          type: "select",
          name: "owner",
          value: "2",
        },
        {
          type: "select",
          name: "investment_readiness",
          value: "EXPLORING",
        },
        {
          type: "select",
          name: "quality",
          value: "POTENTIALLY_NON_FDI",
        },
        {
          type: "select",
          name: "first_response_channel",
          value: "EMAIL",
        },
        {
          type: "text",
          name: "website",
          value: "https://www.caravans.com/",
        },
        {
          type: "select",
          name: "country",
          value: "US",
        },
        {
          type: "select",
          name: "region",
          value: "AMERICAS",
        },
        {
          type: "select",
          name: "primary_sector",
          value: "AUTOMOTIVE",
        },
        {
          type: "select",
          name: "ist_sector",
          value: "ENERGY",
        },
        {
          type: "text",
          name: "first_name",
          value: "Neo",
        },
        {
          type: "text",
          name: "last_name",
          value: "Pug",
        },
        {
          type: "text",
          name: "email",
          value: "neopug@example.com",
        },
        {
          type: "text",
          name: "phone_country_code",
          value: "1234",
        },
        {
          type: "text",
          name: "phone",
          value: "+1 304 314 7000",
        },
        {
          type: "select",
          name: "request_for_call",
          value: "YES_MORNING",
        },
        {
          type: "text",
          name: "google_campaign",
          value: "#r.4123426849_34553257",
        },
        {
          type: "select",
          name: "marketing_channel",
          value: "LINKEDIN",
        },
        {
          type: "select",
          name: "how_they_heard_dit",
          value: "SOCIAL_MEDIA",
        },
        {
          type: "select",
          name: "email_consent",
          value: "False",
        },
        {
          type: "select",
          name: "phone_consent",
          value: "True",
        },
        {
          type: "select",
          name: "first_hpo_selection",
          value: "FOOD_PRODUCTION",
        },
        {
          type: "select",
          name: "second_hpo_selection",
          value: "UK_RAIL",
        },
        {
          type: "select",
          name: "third_hpo_selection",
          value: "LIGHTWEIGHT_STRUCTURES",
        },
        {
          type: "select",
          name: "organisation_type",
          value: "LIMITED_COMPANY",
        },
        {
          type: "select",
          name: "investment_type",
          value: "RETENTION",
        },
        {
          type: "text",
          name: "project_name",
          value: "DEF Hummingbird",
        },
        {
          type: "textarea",
          name: "project_description",
          value: "Expansion of DEF Hummingbird factory sites",
        },
        {
          type: "textarea",
          name: "anonymised_project_description",
          value: "Expansion of more factory sites",
        },
        {
          type: "date",
          name: "estimated_land_date",
          value: "2020-01-02",
        },
        {
          type: "select",
          name: "new_existing_investor",
          value: "EXISTING",
        },
        {
          type: "select",
          name: "investor_involvement_level",
          value: "FDI_HUB_HQ_POST_LEP",
        },
        {
          type: "select",
          name: "specific_investment_programme",
          value: "BUSINESS_PARTNER",
        },
        {
          type: () => {
            cy.autocompleteFakeSelect(
              "client_relationship_manager",
              "Aaron Norris",
              "Aaron Norris",
              "/dh-adviser-search"
            );
          },
          name: "client_relationship_manager",
          value: "Aaron Norris",
        },
        {
          type: "date",
          name: "date_added_to_datahub",
          value: "2020-08-10",
        },
        {
          type: "text",
          name: "project_code",
          value: "67542",
        },
        {
          type: "date",
          name: "project_success_date",
          value: "2026-02-01",
        },
        {
          type: "textarea",
          name: "notes",
          value:
            "This is the notes section. The IST user can add any notes relating to the enquiry. This is a textarea and the user can input multiple lines of text.",
        },
      ]);
      cy.get("input[type=submit]").eq(0).click();

      assertSummaryDetails([
        {
          title: "ABC Electronics Co. (long text)",
          summaryList: [
            { dt: "Date received", dd: "05 May 2024" },
            {
              dt: "Date last updated",
              dd: format(new Date(), "d MMMM yyyy"),
            },
            {
              dt: "Enquiry stage",
              dd: "Engaged in dialogue",
            },
            { dt: "Owner", dd: "James Curran" },
            { dt: "Company in Data Hub", dd: "----" },
          ],
        },
        {
          title: "Enquiry details",
          summaryList: [
            {
              dt: "Enquiry text",
              dd: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure...",
            },
            {
              dt: "Investment readiness",
              dd: "I’m still exploring where to expand my business and would like to know more about the UK’s offer",
            },
            { dt: "Enquiry quality", dd: "Potentially Non-FDI" },
            { dt: "First response channel", dd: "Email" },
          ],
        },
        {
          title: "Company details",
          summaryList: [
            { dt: "Website", dd: "https://www.caravans.com/" },
            {
              dt: "Country",
              dd: "United States",
            },
            { dt: "Region", dd: "Americas" },
            {
              dt: "Company HQ address",
              dd: "ABC Electronics Co. (UK), Far Far Away, United Kingdom",
            },
            { dt: "Primary sector", dd: "Automotive" },
            { dt: "IST sector", dd: "Energy and Environment" },
          ],
        },
        {
          title: "Contact details",
          summaryList: [
            { dt: "First name", dd: "Neo" },
            {
              dt: "Last name",
              dd: "Pug",
            },
            { dt: "Job title", dd: "Director" },
            {
              dt: "Email",
              dd: "neopug@example.com",
            },
            { dt: "Phone", dd: "+1 304 314 7000" },
            { dt: "Call requested", dd: "Yes - morning" },
          ],
        },
        {
          title: "Marketing information",
          summaryList: [
            { dt: "Google campaign", dd: "#r.4123426849_34553257" },
            {
              dt: "Marketing channel",
              dd: "LinkedInLeadGen",
            },
            {
              dt: "How did they hear about DBT?",
              dd: "Other social media (e.g. Twitter/Facebook)",
            },
            {
              dt: "Consent (email)",
              dd: "No",
            },
            { dt: "Consent (telephone)", dd: "No" },
          ],
        },
        {
          title: "HPO details",
          summaryList: [
            { dt: "First HPO selection", dd: "Food production" },
            {
              dt: "Second HPO selection",
              dd: "UK rail",
            },
            { dt: "Third HPO selection", dd: "Lightweight structures" },
          ],
        },
        {
          title: "Data Hub details",
          summaryList: [
            { dt: "Organisation type", dd: "Limited company" },
            {
              dt: "Investment type",
              dd: "Retention",
            },
            { dt: "Project name", dd: "DEF Hummingbird" },
            {
              dt: "Project description",
              dd: "Expansion of DEF Hummingbird factory sites",
            },
            {
              dt: "Anonymised project description",
              dd: "Expansion of more factory sites",
            },
            { dt: "Estimated land date", dd: "02 January 2020" },
            { dt: "New or existing investor", dd: "Existing Investor" },
            {
              dt: "Investor level of involvement",
              dd: "FDI Hub + HQ + Post + LEP",
            },
            {
              dt: "Specific investment programme",
              dd: "Business Partnership (Non-FDI)",
            },
            { dt: "Client Relationship Manager", dd: "Aaron Norris" },
            { dt: "Date added to Data Hub", dd: "10 August 2020" },
            { dt: "Project code", dd: "67542" },
            { dt: "Project success date", dd: "01 February 2026" },
          ],
        },
        {
          title: "Notes",
          summaryList: [
            {
              dt: "Notes",
              dd: "This is the notes section. The IST user can add any notes relating to the enquiry. This is a textarea and the user can input multiple lines of text.",
            },
          ],
        },
      ]);
    });
  });
});
