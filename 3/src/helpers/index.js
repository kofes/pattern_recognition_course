export function name(_class_) {
    return _class_.constructor.name;
}


export function isNumber(n) {
    return !isNaN(parseFloat(n)) && isFinite(n);
}

export function norm2DDistribution(mean1, sigma1, mean2, sigma2, r12) {
    if (r12 !== 1)
        return (x1, x2) => 1 / (2 * Math.PI * sigma1 * sigma2 * Math.sqrt(1 - r12**2)) *
            Math.exp(-1/(2 * (1 - r12**2)) * (
                ((x1 - mean1) / sigma1)**2 -
                2 * r12 * (x1 - mean1) / sigma1 * (x2 - mean2) / sigma2 +
                ((x2 - mean2) / sigma2)**2
            ));
    return (x1, x2) => Math.abs(x1 - x2) < 1e-100 ? 1 / 0.0 : 0;
}

export function reverseNorm2DDistribution(mean1, sigma1, mean2, sigma2, r) {
    let x = t => (t - mean1) / sigma1;
    let y = t => (t - mean2) / sigma2;
    let Xi = t => Math.sqrt(Math.abs(
        -2 * (1 - r**2) * Math.log(2 * Math.PI * sigma1 * sigma2 * Math.sqrt(1 - r**2) * t)
    ));
    return (z, sym = 'x') => {
        if (sym === 'x')
            return t => [
                sigma1 * (r * y(t) - Math.sqrt(Xi(z)**2 + (r**2 - 1) * y(t)**2)) + mean1,
                sigma1 * (r * y(t) + Math.sqrt(Xi(z)**2 + (r**2 - 1) * y(t)**2)) + mean1
            ];
        if (sym === 'y')
            return t => [
                sigma2 * (r * x(t) - Math.sqrt(Xi(z)**2 + (r**2 - 1) * x(t)**2)) + mean2,
                sigma2 * (r * x(t) + Math.sqrt(Xi(z)**2 + (r**2 - 1) * x(t)**2)) + mean2
            ];
        return (t) => console.log(`bad parameter '${t}' at reverseNorm2DDistribution's lambda!`);
    }
}

export function norm2DDistributionDomain(mean1, sigma1, mean2, sigma2, r) {
    return (t, sym = 'x') => {
        let Xi = y => Math.sqrt(Math.abs(
            -2 * (1 - r**2) * Math.log(2 * Math.PI * sigma1 * sigma2 * Math.sqrt(1 - r**2) * y)
        ));
        console.log(`Xi(${t}): `, Xi(t));

        if (sym === 'x')
            return Object.assign({
                min:
                    sigma1 *
                    Xi(t) / Math.sqrt(1 - r**2) *
                    (r**2 - Math.abs(r) - 1)
                    + mean1,
                max:
                    sigma1 *
                    Xi(t) / Math.sqrt(1 - r**2) *
                    (-(r**2) + Math.abs(r) + 1)
                    + mean1
            });
        if (sym === 'y')
            return Object.assign({
                min:
                    sigma2 *
                    Xi(t) / Math.sqrt(1 - r**2) *
                    (r**2 - Math.abs(r) - 1)
                    + mean2,
                max:
                    sigma2 *
                    Xi(t) / Math.sqrt(1 - r**2) *
                    (-(r**2) + Math.abs(r) + 1)
                    + mean2
            });
        return (t) => console.log(`bad parameter '${t}' at reverseNorm2DDistribution's lambda!`);
    }
}

export function translateMatrix(mean, D, r) {
    let result = new Array(mean.length);

    let sum = (arr, end = arr.length) => {
        let acc = 0;
        for (let i = 0; i < end; ++i)
            acc += arr[i];
        return acc;
    };
    let mul = (arr1, arr2) => arr1.map((val, ind) => val * arr2[ind]);

    for (let i = 0; i < mean.length; ++i) {
        result[i] = new Array(mean.length).fill(0);
        result[i][i] = Math.sqrt(D[i] - sum(mul(result[i], result[i]).map((val, k) => val * D[k]), i-1));
        for (let j = 0; j < i; ++j) {
            result[i][j] =
                (
                    Math.sqrt(D[i] * D[j]) * r[i][j] - sum(mul(result[i], result[j]), j-1)
                ) / result[i][i];
        }
    }

    return result;
}

export function if_then(flag, callback) {
    if (flag) return callback();
}

const arr = x => Array.from(x);
const num = x => Number(x) || 0;
const str = x => String(x);
const isEmpty = xs => xs.length === 0;
const take = n => xs => xs.slice(0,n);
const drop = n => xs => xs.slice(n);
const reverse = xs => xs.slice(0).reverse();
const comp = f => g => x => f (g (x));
const not = x => !x;
const chunk = n => xs =>
    isEmpty(xs) ? [] : [take(n)(xs), ...chunk (n) (drop (n) (xs))];

export function numberToWord(n) {
        let a = [
            '', 'one', 'two', 'three', 'four',
            'five', 'six', 'seven', 'eight', 'nine',
            'ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
            'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen'
        ];
        let b = [
            '', '', 'twenty', 'thirty', 'forty',
            'fifty', 'sixty', 'seventy', 'eighty', 'ninety'
        ];
        let g = [
            '', 'thousand', 'million', 'billion', 'trillion', 'quadrillion',
            'quintillion', 'sextillion', 'septillion', 'octillion', 'nonillion'
        ];
        // this part is really nasty still
        // it might edit this again later to show how Monoids could fix this up
        let makeGroup = ([ones,tens,huns]) => {
            return [
                num(huns) === 0 ? '' : a[huns] + ' hundred ',
                num(ones) === 0 ? b[tens] : b[tens] && b[tens] + '-' || '',
                a[tens+ones] || a[ones]
            ].join('');
        };
        // "thousands" constructor; no real good names for this, i guess
        let thousand = (group,i) => group === '' ? group : `${group} ${g[i]}`;
        // execute !
        if (typeof n === 'number') return numberToWord(String(n));
        if (n === '0')             return 'zero';
        return comp (chunk(3)) (reverse) (arr(n))
            .map(makeGroup)
            .map(thousand)
            .filter(comp(not)(isEmpty))
            .reverse()
            .join(' ');
}