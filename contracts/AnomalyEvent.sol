// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

contract AnomalyEvent {
  struct Event {
    uint timestamp;
    string deviceId;
    string description;
  }

  Event[] public events;

  event AnomalyReported(
    uint indexed timestamp, 
    string deviceId, 
    string description
  );

  function reportAnomaly(
    string memory deviceId, 
    string memory description
  ) public {
    events.push(Event(block.timestamp, deviceId, description));
    emit AnomalyReported(block.timestamp, deviceId, description);
  }

  function getEvent(uint index) public view returns (uint, string memory, string memory) {
    Event memory ev = events[index];
    return (ev.timestamp, ev.deviceId, ev.description);
  }

  function getEventsCount() public view returns (uint) {
    return events.length;
  }
}
