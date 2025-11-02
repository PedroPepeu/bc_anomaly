const AnomalyEvent = artifacts.require("AnomalyEvent");

module.exports = function(deployer) {
  deployer.deploy(AnomalyEvent);
};
