// Access and the ability to manage an existing subscription are separate states.
export function billingPresentation(data) {
  if (typeof data?.active !== 'boolean' || typeof data.canPurchase !== 'boolean'
      || typeof data.canManage !== 'boolean' || typeof data.canCancel !== 'boolean' || !Array.isArray(data.plans)
      || (data.canManage && data.billingSource !== 'stripe') || (data.canCancel && !data.canManage)) throw Error('invalid-access');
  const showPlans = !data.active && data.canPurchase;
  return {
    showPlans,
    managementLabel: data.canManage ? (showPlans ? 'billingHistory' : 'manageSubscription') : null,
    showCancellation: data.canCancel,
    message: data.active ? 'active' : data.canPurchase ? 'signedIn'
      : data.canManage ? 'needsPayment' : 'verificationRequired',
  };
}

export function createRefreshFence() {
  let generation = 0;
  return {
    begin: () => ++generation,
    accepts: token => token === generation,
    invalidate: () => { generation++; },
  };
}
