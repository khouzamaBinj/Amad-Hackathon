function levenshteinDistance(a, b) {
  const matrix = [];
  for (let i = 0; i <= b.length; i++) matrix[i] = [i];
  for (let j = 0; j <= a.length; j++) matrix[0][j] = j;

  for (let i = 1; i <= b.length; i++) {
    for (let j = 1; j <= a.length; j++) {
      if (b[i - 1] === a[j - 1]) {
        matrix[i][j] = matrix[i - 1][j - 1];
      } else {
        matrix[i][j] = Math.min(
          matrix[i - 1][j - 1] + 1,
          matrix[i][j - 1] + 1,
          matrix[i - 1][j] + 1
        );
      }
    }
  }

  return matrix[b.length][a.length];
}

const legitDomains = [
  "alrajhibank.com.sa",
  "stcpay.com.sa",
  "alahli.com",
  "riyadbank.com",
  "mada.com.sa"
];

const phishingKeywords = [
  "login", "secure", "verify", "account", "update", "banking",
  "signin", "otp", "mada", "stcpay", "alrajhi", "password"
];

const sensitiveDomains = [
  "alinma.com", "alrajhibank.com.sa", "stcpay.com",
  "alahli.com", "riyadbank.com", "sabb.com", "anb.com.sa",
  "saib.com.sa", "aljazirabank.com.sa", "bankalbilad.com",
  "alawwalbank.com", "bankmuscat.com.sa"
];

const trustedDomains = [
  "alrajhibank.com.sa",
  "alahli.com",
  "alinma.com",
  "riyadbank.com",
  "sabb.com",
  "samba.com",
  "aljazirabank.com.sa",
  "bankalbilad.com",
  "anb.com.sa",
  "saib.com.sa",
  "alawwalbank.com",
  "bankmuscat.com.sa",
  "stcpay.com.sa",
  "mada.com.sa",
  "alfransi.com.sa",
  "bsf.com.sa"
];

function isTrusted(url) {
  try {
    const hostname = new URL(url).hostname;
    return trustedDomains.some(domain => hostname.endsWith(domain));
  } catch {
    return false;
  }
}

function domainLooksSuspicious(domain) {
  return legitDomains.some(legit => {
    const distance = levenshteinDistance(domain, legit);
    return distance > 0 && distance <= 2;
  });
}

function urlHasPhishingKeyword(url) {
  return phishingKeywords.some(keyword =>
    url.toLowerCase().includes(keyword)
  );
}

function isUsingInsecureProtocol(url) {
  const parsed = new URL(url);
  return (
    parsed.protocol === "http:" &&
    sensitiveDomains.some(domain => parsed.hostname.includes(domain))
  );
}

function isSuspicious(url) {
  const parsed = new URL(url);
  const domain = parsed.hostname;
  let score = 0;
  const reasons = [];

  // 🟢 Whitelist check to avoid false positives
  if (trustedDomains.some(trusted => domain.endsWith(trusted))) {
    return {
      suspicious: false,
      score: 0,
      reasons: ["trusted_domain"]
    };
  }

  if (domainLooksSuspicious(domain)) {
    score += 1;
    reasons.push("levenshtein_match");
  }

  if (urlHasPhishingKeyword(url)) {
    score += 1;
    reasons.push("phishing_keyword");
  }

  if (isUsingInsecureProtocol(url)) {
    score += 1;
    reasons.push("http_on_sensitive_domain");
  }

  return {
    suspicious: score >= 2,
    score,
    reasons
  };
}

export { isSuspicious };
