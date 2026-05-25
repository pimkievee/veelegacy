# VeeLegacy Financial Strategy Website

This is a premium static website for VeeLegacy Financial Services, positioned around strategic wealth planning, investment planning, financial protection, retirement planning, estate planning, and business financial strategies.

## Pages
- Home
- About
- Services
- Travel Insurance Quote
- Resources
- Contact / Consultation

## SEO Planning

See `SEO-CONTENT-RECOMMENDATIONS.md` for recommended future landing pages and blog-style guides targeting Ontario, Whitby, RESP, TFSA, RRSP, estate planning, life insurance, newcomers, and family financial planning search intent.

## Travel Insurance Quote Page
The quote page collects client details. To allow a client to receive an instant quote, you need either:
1. a provider quote link that this page can redirect to, or
2. an API/integration from the insurance provider, MGA, or quoting platform.

Without that, the form works as a lead capture form.

## Forms
Forms are set up for Netlify Forms using `data-netlify="true"`.
Deploy on Netlify for easy form submission collection.

## Replace images
Replace:
- `assets/logo.png`
- `assets/profile.jpg`

## GitHub
```bash
git init
git add .
git commit -m "Initial VeeLegacy professional website"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main
```
