module.exports = {
  headerPageNumber: '.header-page-number',
  pageLink: number => `.pagination ol li:nth-child(${number}) a`,
  lastPageLink: '.pagination ol li:last-child a',
}
