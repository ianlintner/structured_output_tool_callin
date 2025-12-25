// Initialize Mermaid diagrams
document$.subscribe(() => {
  mermaid.initialize({
    startOnLoad: true,
    theme: 'default',
    securityLevel: 'loose',
    themeVariables: {
      primaryColor: '#3f51b5',
      primaryTextColor: '#fff',
      primaryBorderColor: '#303f9f',
      lineColor: '#5c6bc0',
      secondaryColor: '#7986cb',
      tertiaryColor: '#9fa8da'
    }
  });
});
